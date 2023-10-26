# opa_ryu_integration
## Commands
### Run OPA
```
./opa run --server --log-format text --set decision_logs.console=true --set bundles.play.polling.long_polling_timeout_seconds=45 --set services.play.url=https://play.openpolicyagent.org --set bundles.play.resource=bundles/WM4kUiAO83
```
### Run Ryu
```
ryu-manager ./ryu_opa_app.py --observe-links
```
### Run mininet
```
sudo mn --topo linear,4 --controller remote,ip=127.0.0.1
```
