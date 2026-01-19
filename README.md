# Change Windows Machine GUID

## Steps

1. Press **Win + R**
2. Paste the following command:
   ```powershell
   powershell -Command "New-Guid | ForEach-Object { Set-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Cryptography' -Name 'MachineGuid' -Value $_.Guid }"
   ```
3. Press **Enter**
