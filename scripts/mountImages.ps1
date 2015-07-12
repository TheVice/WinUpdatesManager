#get-executionpolicy -list
#Set-ExecutionPolicy RemoteSigned -scope CurrentUser

Function GetIsoFiles($aFolderPath)
{
	[string[]]$fileList = @()
	$items = (Get-ChildItem $aFolderPath -Recurse -Name -File -Include *.iso)
	For ($i = 0; $i -lt $items.Count; $i++)
	{
		$fileList += (Get-Item $(Join-Path -Path $aFolderPath -ChildPath $items[$i])).FullName
	}
	$fileList
}

Function MountImagesToDriveLetters([string[]]$aImagePaths)
{
	[string[]]$driveLetters = @()
	For ($i = 0; $i -lt $aImagePaths.Count; $i++)
	{
		$driveLetters += ((Mount-DiskImage -ImagePath $aImagePaths[$i] -StorageType ISO -PassThru) | Get-Volume).DriveLetter
	}
	$driveLetters
}

Function UnMountImagesFromDriveLetters([string[]]$aImagePaths)
{
	For ($i = 0; $i -lt $aImagePaths.Count; $i++)
	{
		Dismount-DiskImage -ImagePath $aImagePaths[$i]
	}
}

Function MountImagesToVolumeIds([string[]]$aImagePaths)
{
	[string[]]$volumeIds = @()
	For ($i = 0; $i -lt $aImagePaths.Count; $i++)
	{
		$volumeIds += (Mount-DiskImage -ImagePath $aImagePaths[$i] -StorageType ISO -NoDriveLetter -PassThru | Get-Volume).ObjectId
	}
	$volumeIds
}

Function MountVolumeToFolder([string[]]$aInput)
{
	$folderPath = $aInput[0]
	$volumeId = $aInput[1]
	mountvol $folderPath $volumeId
}

Function UnMountVolumeFromFolder($aFolderPath)
{
	mountvol $aFolderPath /D
}

[string[]]$isos = GetIsoFiles(".")
If($Args.Count -gt 0)
{
	Write-Output("Unmount images")
	Write-Output($isos)
	UnMountImagesFromDriveLetters($isos)
}
else
{
	Write-Output("Images to mount")
	Write-Output($isos)
	[string[]]$driveLetters = MountImagesToDriveLetters($isos)
	Write-Output("Drive letters")
	Write-Output($driveLetters)
}
