# crappy: Gandcrab v5.2 decryption scripts

This repository contains Python3 scripts that can decrypt files encrypted with
the Gandcrab 5.2 ransomware. Please note that this is a proof-of-concept which
could be used to make a proper "one-click" tool.

It uses the RSA private master key released by FBI/Europol on 2019/07/15
(https://assets.documentcloud.org/documents/6199678/GandCrab-Master-Decryption-Keys-FLASH.pdf).

## /!\ WARNING /!\

Even if these scripts do not erase the original encrypted data, it is highly
recommended to make backup of your encrypted data and hard drive before running
them. 

As stated in the GPL license attached, the author could not be taken
responsible for any loss of data due to the usage of these scripts.

## General usage

Decryption happens in two steps. The first one recover the "user" private RSA
key that has been encrypted thanks to the so-called master key (originally only
owned by the ransomware authors). The second one uses this recovered RSA
private key to decrypt the files.

### RSA private user key decryption

The RSA private user key is contained in the ransom, within the `GANDCRAB KEY` block.

The tool in `scripts/decr_priv_user_rsa_key.py` is in charge of extracting and
decrypting this key:

    $ python3 ./scripts/decr_priv_user_rsa.py 
    Usage: ./scripts/decr_priv_user_rsa.py ransom.txt rsa_user_private_file

The RSA private user key will be written in the path given at `rsa_user_private_file`.

### File decryption

Once the private RSA user key has been found, files can be decrypted thanks to
the tool in `scripts/decr_file.py`:

    $ python3 ./scripts/decr_file.py
    Usage: ./scripts/decr_file.py rsa_user_private_file encrypted_file

The decrypted file will be written in the same directory as the original one, without the Gandcrab specific extension.

### (Optional) PC Data decryption

The PC Data block in the ransom can be decrypted thanks to the `scripts/pcdata.py` tool:

    $ python3 ./scripts/pcdata.py 
    Usage: ./scripts/pcdata.py ransom.txt

## Example

A sample of an encrypted file and a ransom file is in the `sample_run` directory.

Let's decrypt this file:

    $ pip3 install -r scripts/requirements.txt
    $ python3 ./scripts/decr_priv_user_rsa.py sample_run/PYFCVQHUYJ-MANUAL.txt sample_run/rsa_user_priv
    [+] Priv key size: 1172
    [+] Salsa key: 74a92580b32a57cb2b9a3636a0ad141224fb6676da4e14c0edda1d0c73d091c2
    [+] Salsa nonce: 77dd722df221ec2e
    [+] Decrypting RSA private user key...
    [+] RSA private key details:
    [+] p  = 0xf6123f1dbaa941ffb14abf1c130bc7e4b4293d0d7eedb37d02fa232c56e7879e7111f01d8fb5af57d550aba2d1d4b6be661794aa812575e7ab0cfd2cffac529047798e08f89cecb43e7791dcf3ba74dd9b311d2187358e991b7e67072e07871a535361d38740a97b29beb89fcf8fea96b9ea22ee02636c86b8ed574ba977716b
    [+] q  = 0xe0866584b95b4e289ae2b2f12e6740b141e4e0aed4b520e2cf489e31a3c12a560178e0fdde2d65b320d8d9f865261e6843bda1cbff45b89ecf715fd54371e6f9e31368a7d86805f84606dd5b8c383f1528b6b6a1b8de8098e371c6410380c722bf552a51b4ce173a31416e183fc2f2770b3a9e415016c21b1f6c0cba2139a503
    [+] d  = 0x8bc973b00c831e1d8214cef30779223f80777c39fbba2ae073ff4982861c5990d4af5476c87480fdc84d8dfff93dd840a837a703e72bb194cfc0b9da257489cc6c677e03a512bdb6326300e5c8184ecfd8b51b8924ee4a0cee578b8fe297ce3e21af444fb5e1cc1c10b02791fcb6693ddd8566884a037ceedde725390d6c99185d78988b12556e91c1b4828e2f6801da38e64b4d51fd2b4a7de102478aba832dc4fa31e9632437ac31db0bfc631e04a50d1b4172d78a22dd12e3ae99b9f509d042315d0bc31905413f2ce502742a7ebdcf802e5a0031e537c132e8fd42a096e51a9983ba877c7e17b555e5162f0629d0c3b0834d6b11d93e0a5179bbd464c515
    [+] dp = 0x7af192e75fa3c17de72ed95d4586d550c752f35612dce098cd2bfcf6e254bbc5c5e89877ac9db205c8668ddac3cbeba22590128f3e07616966650ef9b4a47c7be9ba29e501922611c8442574a7b1b9421f8fe266260ff4373b2d647c89dae8fd96344ae44ce759c6578d1ae17deb01e25cf14692744f08a227332e3277715e11
    [+] dq = 0x3856e1107de6806546004ec0a0513e757c406f74cf61280061dd29fcf0c75ed538075a05ba03903a73aa967f72fa2eb521126b9021dd1fe791cc342cf2809961e8ee0cdbd93cb90ac49fa259ff8479a7d89088a16a1f430b9a3f096d74f092879095514a31616988aba56c77df400ed17a5ada2d2f68968a71c70e268281d17b
    [+] iq = 0x2d3828289384001d1023c6b686b97f169cd90ec0e13d11fdb399d348c9520c91041ffe2eb043734069ac3b7f66dd20f12736de18f3525191389af9f8732e57226048268100c5c01da3a85d0ea2e81d60b7278ab4ab29ddc07926a4e1bfba7e8a1ab4dc09ef450fd372c9f64b2de033a0bc16057d74d5debf844604ec84e4f535
    [+] N  = 0xd7d1265bd35e078acfb3959799115f7a15ca0133f46bfd9451e570021edbd1c98e45d4c5ab81319ad2d7f9c2e75cfc3ef09e0cb8e47168356aa08f8cb004a08b77fe5fccaf4ae69c2f751229d2c5111920970935e34102f4d6e421999938c8e26b2cd6b696b19e3a77913a7b2fa6c7d3385a63b2e1c11debb7b0f185756f5c7b9427b2f18eda0bae42b90f3005d61d53b4a60849b52cb1d0e31d1e47c934fe8c1c2e7478d89c72e0c479e624b5f8dbefa1941eb8696c591da80013743c26af3e74bd25160cbf297bad4e10134d974202c8d0878a7adf25dce2db5f331ea31c07d48a08a389c9ce773f47e23bec58eadb97545afcb0aada31dcfa571204534b41
    [+] RSA private user key written to 'sample_run/rsa_user_priv'
    $ python3 ./scripts/decr_file.py sample_run/rsa_user_priv sample_run/test.docx.pyfcvqhuyj
    [+] Salsa20 key = a835c775aa03384d7fc99e40323ed085a41212ac4d526ac986d45937b16fd56b
    [+] Salsa20 nonce = e49db67c8dbb2401
    [+] Decrypting file...
    [+] Decrypted file written to 'sample_run/test.docx'.
    $ file sample_run/test.docx
    sample_run/test.docx: Microsoft Word 2007+


(Optional) Let's show the PC data block:

    $ python3 ./scripts/pcdata.py sample_run/PYFCVQHUYJ-MANUAL.txt 
    pc_user=user&pc_name=WIN-ADNGVE2JIMV&pc_group=WORKGROUP&pc_lang=fr-FR&pc_keyb=0&os_major=Windows 7 Home Basic&os_bit=x86&ransom_id=c8f971da40208fca&hdd=C:FIXED_10735316992/7081914368,Z:REMOTE_0&id=200&sub_id=1745&version=5.2&action=call
