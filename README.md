# Hydra_ML
## Description
Utility package that allows to embedd tune samplers in hydra configs.

### Supported tags
- "#choice:1,2,3,..."
- "#loguniform:\<start\>,\<end\>"
- "#grid:1,2,3,..."

## Example usage
#### **`conf/config.yaml`**
```yaml
training:
    batch_size: "#choice:2,4,8,16"
    learning_rate: "#loguniform:1e-5,1e-3"
    hidden_size: "#grid:100,200,400"
    name: "Test"
```
#### **`main.py`**
```python
@ hydra.main(config_path="conf", config_name="config")
def main(cfg):
    cfg = OmegaConf.to_container(cfg, resolve=True)
    cfg = apply_tune(cfg)
```
