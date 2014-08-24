#get-executionpolicy -list
#Set-ExecutionPolicy RemoteSigned -scope CurrentUser

Function Get-InstalledUpdate()
{
	[string[]]$updates = @()
	[object[]]$tmpUpdates = $(Get-WmiObject Win32_QuickFixEngineering | Select-Object HotFixID)
	For ($i = 0; $i -lt $tmpUpdates.Count; $i++)
	{
		[string]$up = ($tmpUpdates[$i].HotFixID)
		If ([char]::isDigit($up[$up.length-1])) # KB917607
		{
			$updates += $up
		}
		Else # KB2712101_Microsoft-Windows-CameraCodec-Package | KB2899189_Microsoft-Windows-CameraCodec-Package
		{
			$j = $up.Length - 1
			For ( ; $j -ne 0; $j--)
			{
				If ([char]::isDigit($up[$j]))
				{
					break
				}
			}
			$updates += $up.Substring(0, $j + 1)
		}
	}
	$updates
}

Function Get-LocatedUpdates()
{
	[string[]]$fileList = @()
	[object]$path = $(Get-ChildItem env:temp | Select-Object Value)

	If (Test-Path $path.Value -PathType Container)
	{
		[string[]]$items = (Get-ChildItem $path.Value -Name -File -Include *.msu)
		For ($j = 0; $j -lt $items.Count; $j++)
		{
			$fileList += (Get-Item $(Join-Path -Path $path.Value -ChildPath $items[$j])).FullName
		}
	}
	$fileList
}

[string[]]$installedUpdates = Get-InstalledUpdate
[string[]]$avalibleUpdates = Get-LocatedUpdates
[string[]]$updatesToInstall = @()

For ($i = 0; $i -lt $avalibleUpdates.Count; $i++)
{
	$present = $false
	For ($j = 0; $j -lt $installedUpdates.Count; $j++)
	{
		If ($avalibleUpdates[$i].IndexOf($installedUpdates[$j]) -ne -1)
		{
			$present = $true
			break
		}
	}
	If ($false -eq $present)
	{
		$updatesToInstall += $avalibleUpdates[$i]
	}
}

Write-Output($updatesToInstall)
