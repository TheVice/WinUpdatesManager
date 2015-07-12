#get-executionpolicy -list
#Set-ExecutionPolicy RemoteSigned -scope CurrentUser

Function Get-InstalledUpdates()
{
	[string[]]$updates = @()
	[object[]]$hotFixIDs = $(Get-WmiObject Win32_QuickFixEngineering | Select-Object HotFixID)

	For ($i = 0; $i -lt $hotFixIDs.Count; $i++)
	{
		[string]$up = ($hotFixIDs[$i].HotFixID)
		$updates += $up
	}

	$updates
}

[string[]]$installedUpdates = Get-InstalledUpdates
Write-Output($installedUpdates)
