# Python ACES adaptation

## Installation

```sh
install and sync relay server
git clone https://github.com/galperins4/PythAces 
cd ~/PythAces
pip3 install setuptools
pip3 install -r requirements.txt
npm install 
sudo npm install pm2@latest -g
```

## Configuration & Usage 

After the repository has been cloned you need to open the `config.json` / `coin.json` and change it to your liking. Once this has been done execute the pm2 command `pm2 start apps.json`to start the script. 

As the script leverages @FaustBrians ARK python client as well as database retreival and storage classes, python 3.6+ is required. In addition it is required  to run this alongside an ark/kapu elay node given the DB interaction and little reliance on the API.

## Available Configuration Options (config.json)
- channel: dpos channel for inbound transactions (currently support ark/dark, kapu/dkapu, persona-t)
- channel_ip: ip address of node
- service_acct: service account for inbound transactions for the channel 
- db_username: os username
_ flat_fee: flat fee per transaction
- pct_fee: percentage fee per transaction
- reach: how many peers to broadcast tx to (NOT CURRENTLY IN USE)

## Available Configuration Options (coin.json) - per coin supported 
- relay_ip: relay to broadcast outbound transactions
- service_acct: outbound service account 
- service_account_passphrase: passphrase 
- service_account_secondphrase: secondphrase 
- addr_start: letter addresses start with

Note: Pythaces runs on port 5000

## To Do 
- Add more features as necessary
- Additional exception handling and validators
- Add more dpos coins
- Add non-DPOS coins 

### .01
- Initial release

## Support

If you like this project and it helps you in your every day work I would greatly appreciate it if you would consider to show some support by donating to one of the below mentioned addresses.

- BTC - 38jPmBCdu9C5SBPbeb4BTBQG2SAbGvbfKf
- ETH - 0x9c3BB145C6bCde9BC502B90B8C32C0aa26714394
- ARK - AMhTN98yvWP8SJNyxmgEfg9ufuxHyapW73

## Security

If you discover a security vulnerability within this package, please open an issue. All security vulnerabilities will be promptly addressed.

## Credits

- [galperins4](https://github.com/galperins4)
- [All Contributors](../../contributors)

## License

[MIT](LICENSE) © [galperins4](https://github.com/galperins4)





