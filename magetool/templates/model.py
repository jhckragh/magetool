string = """<?php

class ${namespace}_${module_name}_Model_${name} extends ${superclass}
{
    protected function _construct()
    {
        $$this->_init('${group}/${name_lower}');
    }
}
"""
