# Policy integration between OPA and Ryu
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

## Sample Rego Policy
### Playground link
[https://play.openpolicyagent.org/p/2v2hWn3g2R]
### Rules
```
package ryu_policy

default allow = false

# Allow port 22 and 80
allow {
    input.port == 22
} else {
    input.port == 80
}
```
### Sample input
```
{
    "port": 23
}
```

## Extra
### View all flows
```
for sw in $(ovs-vsctl list-br); do echo "Flows for $sw:"; ovs-ofctl dump-flows $sw; echo ""; done
```
### Remove all flows except Controller flows from a particular switch (S1)
```
ovs-ofctl dump-flows s1 | grep -v "actions=controller" | awk -F ',' '{print $1}' | awk '{print $NF}' | xargs -I {} ovs-ofctl del-flows s1 cookie={}
```
### Remove flows except controller flows for all switches
```
for sw in $(ovs-vsctl list-br); do ovs-ofctl dump-flows $sw | grep -v "actions=controller" | awk -F ',' '{print $1}' | awk '{print $NF}' | xargs -I {} ovs-ofctl del-flows $sw cookie={}; done
```
