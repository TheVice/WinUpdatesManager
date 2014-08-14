#get-executionpolicy -list
#Set-ExecutionPolicy RemoteSigned -scope CurrentUser

Function GetIsoFiles()
{
	[string[]]$fileList = @()
	$subDirectories = (Get-ChildItem -Name -Directory)
	For ($i = 0; $i -lt $subDirectories.Count; $i++)
	{
		If ($subDirectories[$i].Length -eq 4)
		{
			$items = (Get-ChildItem $subDirectories[$i] -Name -File -Include *.iso)
			For ($j = 0; $j -lt $items.Count; $j++)
			{
				$fileList += (Get-Item $($subDirectories[$i] + "\" + $items[$j])).FullName
			}
		}
	}
	$fileList
}

Function GetAddonFolders()
{
	[string[]]$folderList = @()
	$addonsPath = (Get-Item "Addons").FullName
	$subDirectories = (Get-ChildItem $addonsPath -Name -Directory)
	For ($i = 0; $i -lt $subDirectories.Count; $i++)
	{
		If ($subDirectories[$i].Length -eq 4)
		{
			$folderList += (Get-Item $($addonsPath + "\" + $subDirectories[$i])).FullName
		}
	}
	$folderList
}

Function MountImages([string[]]$aImagePaths)
{
	[string[]]$mountPoints = @()
	For ($i = 0; $i -lt $aImagePaths.Count; $i++)
	{
		$mountPoints += ((Mount-DiskImage -ImagePath $aImagePaths[$i] -StorageType ISO -PassThru) | Get-Volume).DriveLetter
	}
	$mountPoints
}

Function UnMountImages([string[]]$aImagePaths)
{
	For ($i = 0; $i -lt $aImagePaths.Count; $i++)
	{
		Dismount-DiskImage -ImagePath $aImagePaths[$i]
	}
}

#$isos = GetIsoFiles
#Write-Output($isos)

#$addons = GetAddonFolders
#Write-Output($addons)

#Write-Output(MountImages($isos))
#UnMountImages($isos)
