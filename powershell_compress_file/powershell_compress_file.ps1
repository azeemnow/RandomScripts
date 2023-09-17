##The script will prompt you to enter the name of the file to compress.

## Once you enter the file name, the script will compress the file and create a .zip file with the same name in the current directory.

###############################################################

 

# Get the name of the file to compress

$fileName = Read-Host "Enter the name of the file to compress: "

 

# Get the current directory

$currentDirectory = Get-Location

 

# Create a zip file with the same name as the original file

$zipFileName = $fileName + ".zip"

 

# Compress the file

Compress-Archive -Path $fileName -DestinationPath $zipFileName

 

# Write a message to the console

Write-Host "The file '$fileName' has been compressed to '$zipFileName'."