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

Function MountImages2([string[]]$aImagePaths)
{
	[string[]]$volumeIds = @()
	For ($i = 0; $i -lt $aImagePaths.Count; $i++)
	{
		$volumeIds += (Mount-DiskImage -ImagePath $aImagePaths[$i] -StorageType ISO -NoDriveLetter -PassThru | Get-Volume).ObjectId
	}
	$volumeIds
}

Function UnMountImages([string[]]$aImagePaths)
{
	For ($i = 0; $i -lt $aImagePaths.Count; $i++)
	{
		Dismount-DiskImage -ImagePath $aImagePaths[$i]
	}
}

Function GetFolderNameForImage($aImagePath)
{
	$folderName = ""
	$beginIndex = $aImagePath.LastIndexOf("-") + 1
	$endIndex = $aImagePath.LastIndexOf(".")
	$len = $endIndex - $beginIndex

	If ($len -eq 6) #Windows-KB913086-201101.iso
	{
		$folderName = $aImagePath.Substring($beginIndex, $len)
	}
	ElseIf ($len -eq 1) #Windows-KB913086-201102-1.iso
	{
		$baseName = $aImagePath.Substring(0, $beginIndex - 1)
		$baseName += "."
		$baseName = GetFolderNameForImage($baseName)
		$additionName = $aImagePath.Substring($beginIndex - 1, $len + 1)
		$folderName = $baseName + $additionName
	}
	ElseIf ($len -eq 2) #Windows-KB913086-2013-01.iso
	{
		$baseName = $aImagePath.Substring(0, $beginIndex - 1)
		$baseName = $baseName.Substring($baseName.LastIndexOf("-") + 1)
		$additionName = $aImagePath.Substring($beginIndex - 1, 3)
		$folderName = $baseName + $additionName
	}
	$folderName
}

Function MountVolumeOfImage()
{
	[string[]]$mountedFolders = @()
	$rootPath = $args[0][0]
	[string[]]$imagePaths = $args[0][1]
	[string[]]$volumeIds = $args[0][2]

	If ((Test-Path $rootPath -PathType Container) -and ($imagePaths.Count -eq $volumeIds.Count))
	{
		For ($i = 0; $i -lt $imagePaths.Count; $i++)
		{
			$folderPath = $rootPath + "\" + (GetFolderNameForImage $imagePaths[$i])
			If ((Test-Path $folderPath) -eq $false)
			{
				Write-Output("Create folder - " + (New-Item -Path $folderPath -ItemType Directory).FullName)
			}
			If ((Test-Path $folderPath -PathType Container) -and ((Get-ChildItem $folderPath) -eq $null))
			{
				mountvol $folderPath $volumeIds[$i]
				If ((Get-ChildItem $folderPath) -ne $null)
				{
					$mountedFolders += $folderPath
				}
				Else
				{
					Write-Output("mountvol not mounted image " + $imagePaths[$i] + " with Volume id " + $volumeIds[$i] + " to folder " + $folderPath)
				}
			}
			Else
			{
				Write-Output("Incorect condition - " + $folderPath + ": path set to file or path to non empty folder")
			}
		}
	}
	$mountedFolders
}

Function UnMountVolumeOfImage($aMountedFolders)
{
	For ($i = 0; $i -lt $aMountedFolders.Count; $i++)
	{
		mountvol $aMountedFolders[$i] /D
	}
}

#http://stackoverflow.com/questions/894430/powershell-hard-and-soft-links#comment9823010_5549583
Function mklink { cmd /c mklink $args }

Function rmlink($aPath)
{
	If (Test-Path $aPath)
	{
		If(Test-Path $aPath -PathType Container)
		{
			cmd /c rd $aPath
		}
		Else
		{
			cmd /c del $aPath
		}
	}
}

Function linkingSubFolders()
{
	[string[]]$linkedObjects = @()
	$rootPath = $args[0][0]
	[string[]]$paths = $args[0][1]

	For ($i = 0; $i -lt $paths.Count; $i++)
	{
		[string[]]$subFolders = (Get-ChildItem $paths[$i] -Name -Directory)
		For ($j = 0; $j -lt $subFolders.Count; $j++)
		{
			$link = $rootPath + "\" + $subFolders[$j]
			$target = $paths[$i] + "\" + $subFolders[$j]
			Write-Output("link - " + $link + " target - " + $target)
			mklink /J $link $target
			$linkedObjects += $link
		}
	}
	$linkedObjects
}

Function unLinkingSubFolders($aLinkPaths)
{
	For ($i = 0; $i -lt $aLinkPaths.Count; $i++)
	{
		rmlink $aLinkPaths[$i]
	}
}

Function prepareLinkFolder($aRootPath)
{
	$folderPath = $aRootPath + "\0"
	If ((Test-Path $folderPath) -eq $false)
	{
		Write-Output("Create folder - " + (New-Item -Path $folderPath -ItemType Directory).FullName)
	}
	$folderPath
}

If (($args -ne $null) -and ($args[1] -ne "clean"))
{
	$rootPath = $args[0]
	$folderForLinking = prepareLinkFolder($rootPath)

	[string[]]$isos = GetIsoFiles
	[string[]]$volumes += MountImages2($isos)
	[string[]]$mountedPoints = MountVolumeOfImage($rootPath, $isos, $volumes)
	#linkingSubFolders($folderForLinking, $mountedPoints)

	#unLinkingSubFolders($linkObjects)
	UnMountVolumeOfImage($mountedPoints)
	UnMountImages($isos)

	#[string[]]$addons = GetAddonFolders
	#linkingSubFolders($folderForLinking, $addons)

	#unLinkingSubFolders($linkObjects)
}
#Else
#{
#}
