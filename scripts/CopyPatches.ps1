#get-executionpolicy -list
#Set-ExecutionPolicy RemoteSigned -scope CurrentUser

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

Function GetPatchesForVersion()
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

If($Args.Count -lt 2)
{
    Write-Output("Bad Using")
    Write-Output("Use next (for example):`n ?: <Target version> <Path where to copy patches>")
    Exit
}

$targetVersion = $Args[0] # "Windows8" | "Windows8.1"
$targetPath = $Args[1] # "A:\Win8 SP1"

$disks = Get-CompactDisks
ForEach ($disk in $disks)
{
    $currenTargetPath = Join-Path -Path $targetPath -ChildPath $disk.VolumeName
    $files = GetPatchesForVersion $disk.DeviceID $targetVersion
    ForEach ($file in $files)
    {
        $targetFile = Split-Path -Path $file -NoQualifier
        $targetFile = Join-Path -Path $currenTargetPath -ChildPath $targetFile
        If (!(Test-Path -Path $targetFile))
        {
            New-Item $targetFile -Force
            Write-Host ("Copy {0} to {1}" -f $file, $targetFile)
            Copy-Item -Path $file -Destination $targetFile -Recurse -Force
        }
        Else
        {
            Write-Host ("File {0} already exists {1}" -f $file, $targetFile)
        }
    }
}
