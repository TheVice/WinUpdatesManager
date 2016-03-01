# Get-ExecutionPolicy -Scope CurrentUser
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Function Get-CompactDisks()
{
	$compactDisks = @()
	$disks = Get-WMIObject win32_logicaldisk | Select-Object -Property DeviceID, DriveType, FileSystem, VolumeName
	ForEach ($disk in $disks)
	{
		if (($disk.DriveType -eq 5) -and ($disk.FileSystem -eq "CDFS"))
		{
			$compactDisks += $disk
		}
	}
	$compactDisks
}

Function Get-PatchesForVersion()
{
	param($aSrcPath, $aVersion)

	[string[]]$fileList = @()
	[string[]]$folderList = @()
	$folderList = Get-ChildItem -Path $aSrcPath -Directory -Filter $aVersion -Recurse -Name

	For ($i = 0; $i -lt $folderList.Count; $i++)
	{
		$pathToFolder = Join-Path -Path $aSrcPath -ChildPath $folderList[$i]
		[string[]]$subFileList = @()
		$subFileList = Get-ChildItem -Path $pathToFolder -Recurse -Name -File

		For ($j = 0; $j -lt $subFileList.Count; $j++)
		{
			$subFileList[$j] = Join-Path -Path $pathToFolder -ChildPath $subFileList[$j]
		}

		$fileList += $subFileList
	}

	$fileList
}

Function Get-AddonSourceAndTargetPaths()
{
	param($aSrcPath)

	$sourceAndTarget = New-Object 'System.Collections.Generic.HashSet[System.Tuple[string, string]]'
	[string[]]$folderList = @()
	$folderList = Get-ChildItem -Path $aSrcPath -Directory -Name
	ForEach ($folder in $folderList)
	{
		$sourcePath = Join-Path -Path $aSrcPath -ChildPath $folder
		$t = [System.Tuple]::Create($sourcePath, $folder)
		$tmp = $sourceAndTarget.Add($t)
	}

	$sourceAndTarget
}

If ($Args.Count -lt 2)
{
	Write-Output("Bad Using")
	Write-Output("Use next (for example): <Target version> <Path where to copy patches>")
	Write-Output("Use next (for example): <Target version> <Path where to copy patches> <Path where patches exists>")
	Exit
}

$targetVersion = $Args[0] # "Windows8" | "Windows8.1"
$targetPath = $Args[1] # "A:\Win8 SP1"

If ($Args.Count -eq 2)
{
	$disks = Get-CompactDisks
	ForEach ($disk in $disks)
	{
		$currentTargetPath = Join-Path -Path $targetPath -ChildPath $disk.VolumeName
		$files = Get-PatchesForVersion $disk.DeviceID $targetVersion
		ForEach ($file in $files)
		{
			$targetFile = Split-Path -Path $file -NoQualifier
			$targetFile = Join-Path -Path $currentTargetPath -ChildPath $targetFile
			If (!(Test-Path -Path $targetFile))
			{
				Write-Host("Copy {0} to {1}" -f $file, $targetFile)
				$tmp = New-Item $targetFile -Force
				Copy-Item -Path $file -Destination $targetFile -Recurse -Force
			}
			Else
			{
				Write-Host("File {0} already exists {1}" -f $file, $targetFile)
			}
		}
	}
}
ElseIf ($Args.Count -eq 3)
{
	$pathToAddonFolder = $Args[2] # "A:\Addons"
	$sourceAndTarget = Get-AddonSourceAndTargetPaths $pathToAddonFolder
	ForEach ($i in $sourceAndTarget)
	{
		$currentTargetPath = Join-Path -Path $targetPath -ChildPath $i.Item2
		$files = Get-PatchesForVersion $i.Item1 $targetVersion
		ForEach ($file in $files)
		{
			$targetFile = $file.Substring($pathToAddonFolder.Length + 1 + $i.Item2.Length)
			$targetFile = Join-Path -Path $currentTargetPath -ChildPath $targetFile
			If (!(Test-Path -Path $targetFile))
			{
				Write-Host("Copy {0} to {1}" -f $file, $targetFile)
				$tmp = New-Item $targetFile -Force
				Copy-Item -Path $file -Destination $targetFile -Recurse -Force
			}
			Else
			{
				Write-Host("File {0} already exists {1}" -f $file, $targetFile)
			}
		}
	}
}
