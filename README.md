# Steps

## 0. Download Malwarebytes
- FYI: If Malwarebytes is already installed on your system, then skip this step.
- ⬇️ Direct download link: [MBSetup.exe](https://data-cdn.mbamupdates.com/web/mb5-setup-consumer/MBSetup.exe)

## 1. Quit Malwarebytes
<img width="1129" height="736" alt="image" src="https://github.com/user-attachments/assets/d95eb02f-b5c3-400c-b0e4-a820d283e6f7" />

## 2. Spoof 'MachineGuid' in registry
1. Press **[Win]** + **[R]**
2. Paste the following command:
   ```powershell
   powershell -Command "New-Guid | ForEach-Object { Set-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Cryptography' -Name 'MachineGuid' -Value $_.Guid }"
   ```
3. Press **[Enter]**

## 3. Open Malwarebytes
<img width="919" height="751" alt="image" src="https://github.com/user-attachments/assets/8a0578e5-8b95-45a2-a69a-de25aa603b4e" />

## 4. Setup Malwarebytes
- DO NOT click: "Activate subscription" or "Buy now"

<img width="1024" height="720" alt="image" src="https://github.com/user-attachments/assets/7c5ca2ea-68b0-45f6-8f08-cf9801b9c807" />
<img width="1024" height="720" alt="image" src="https://github.com/user-attachments/assets/af86b3de-9585-4750-94d9-5806ac799fa5" />
<img width="1024" height="720" alt="image" src="https://github.com/user-attachments/assets/1d19d731-42bd-4ba9-bcfa-a12e3307fa2c" />

## 5. You're finished!
- Your premium trial has now been reset back to 14 days!
