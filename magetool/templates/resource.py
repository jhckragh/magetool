string = """<?php

class ${namespace}_${module_name}_Model_Mysql4_${name} extends ${superclass}
{
    protected function _construct()
    {
        $$this->_init('${group}/${name_lower}', '${group}_id');
    }
}
"""
