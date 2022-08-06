def set_env_output(name, value):
    print(f"Output - {name} : {value}")
    print(f"::set-output name={name}::{value}")

