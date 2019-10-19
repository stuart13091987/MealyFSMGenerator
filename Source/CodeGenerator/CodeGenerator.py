import os
import errno
from SMInfoParser.StateMachineInfo import StateJumpInfo
import re
import shutil


class CodeGenerator:
    """
    This file help generates .c and .h code for the state machine
    """

    _sm_name = None
    _priv_func_name_list = []
    _priv_condi_name_list = []
    _priv_state_name_list = []

    def __init__(self, state_machine_name=None):
        if state_machine_name is None:
            raise ValueError("PLease Provide state machine name\n")
        else:
            self._sm_name = "Default"

    def write_file(self, st_list):
        raise NotImplementedError("Please implement in your code generator")

    def _prepare_st_list(self, st_list):
        # check input
        assert isinstance(st_list, list)
        for item in st_list:
            assert isinstance(item, StateJumpInfo)
            if item.action is not None:
                if "NULL" not in item.action:
                    item.action = "SM_" + item.action
                    if item.action not in self._priv_func_name_list:
                        self._priv_func_name_list.append(item.action)
                item.from_state = sm_state_common(self._sm_name) + self.__get_str_without_nr(item.from_state)
                item.to_state = sm_state_common(self._sm_name) + self.__get_str_without_nr(item.to_state)
                if item.from_state not in self._priv_state_name_list:
                    self._priv_state_name_list.append(item.from_state)

                condition_prefix = sm_condition_common(self._sm_name)
                if item.condition not in self._priv_condi_name_list:
                    self._priv_condi_name_list.append(item.condition)
                item.condition = condition_prefix + self.__get_str_without_nr(item.condition)

        self._priv_condi_name_list.sort(key=lambda x: int(re.findall(r"^\d*", x)[0]))
        for i in range(0, len(self._priv_condi_name_list)):
            self._priv_condi_name_list[i] = sm_condition_common(self._sm_name) + \
                                            self.__get_str_without_nr(self._priv_condi_name_list[i])

        for item in st_list:
            item.print()

        return st_list
