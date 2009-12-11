# "Mysql4_" is considered part of ${name}
string = """<?php

class ${namespace}_${module_name}_Model_${name} extends ${superclass}
{
    protected function _construct()
    {
        $$this->_init('${group}/${end}', '${id_field_name}');
    }
}
"""
