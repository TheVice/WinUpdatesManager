#Get-ExecutionPolicy -list
#Set-ExecutionPolicy RemoteSigned -scope CurrentUser

Function Generate-MonthYearNames()
{
	[string[]]$monthYear = @()
	$startYear = 16

	For ($i = $startYear; $i -gt -1; $i--)
	{
		$year = ""
		if ($i -lt 10)
		{
			$year = "0{0}" -f $i
		}
		else
		{
			$year = $i
		}

		For ($month = 12; $month -gt 0; $month--)
		{
			if ($month -lt 10)
			{
                $monthYear += ("DLC_0{0}{1}" -f $month, $year)
				$monthYear += ("0{0}{1}" -f $month, $year)
			}
			else
			{
                $monthYear += ("DLC_{0}{1}" -f $month, $year)
				$monthYear += ("{0}{1}" -f $month, $year)
			}
		}
	}

	$monthYear
}

Function Get-PathsToPatches()
{
    param($aSrcPath, $aMonthAndYear)

    [string[]]$fileList = @()
    [string[]]$folderList = @()
    $folderList = Get-ChildItem -Path $aSrcPath -Directory -Name
    ForEach ($my in $aMonthAndYear)
    {
    	ForEach ($folder in $folderList)
    	{
    		If ($my -eq $folder)
    		{
                $pathToFolder = Join-Path -Path $aSrcPath -ChildPath $folder
                [string[]]$subFileList = @()
                $subFileList = Get-ChildItem -Path $pathToFolder -Recurse -Name -File
                
                For ($j = 0; $j -lt $subFileList.Count; $j++)
                {
                    $subFileList[$j] = ".\{0}\{1}" -f $folder, $subFileList[$j]
                }

                $fileList += $subFileList
                $fileList += ""
    		}
    	}
    }

    $fileList
}


If($Args.Count -lt 1)
{
    Write-Output("Bad Using")
    Write-Output("Use next (for example):`n ?: <Path where folders with patches located>")
    Exit
}

$sourcePath = $Args[0]

[string[]]$monthYear = Generate-MonthYearNames
[string[]]$paths = Get-PathsToPatches $sourcePath $monthYear

ForEach ($path in $paths)
{
    Write-Host $path
}
