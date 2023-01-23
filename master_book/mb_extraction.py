import dataclasses

import pandas as pd
import numpy as np
from enum import Enum

PATH = r'it_masterbook.xlsx'


class EffectType(Enum):
    NPV = 1
    UMV = 2
    DMV = 4


@dataclasses.dataclass
class CalculationData:
    effect: pd.Series
    costs: pd.Series


@dataclasses.dataclass
class Project:
    data: pd.DataFrame
    code: str
    project_name: str
    programme: str
    version: str
    made_by: str
    start_date: pd.Timestamp


class ProjectCalculationAdapter:

    def __init__(self, project):
        self.project = project

    def get_calculation(self, effect_types):
        effect = 0
        for effect_type in effect_types:
            match EffectType:
                case EffectType.DMV:
                    effect += project.data['DMV, тыс.руб.']
                case EffectType.UMV:
                    effect += project.data['UMV, тыс.руб.']
                case EffectType.NPV:
                    effect += project.data['NPV, тыс.руб.']
        return CalculationData(effect=effect, costs=project.data['Costs'])


class ProjectFactory:

    @classmethod
    def from_excel(cls, data_path):
        sheet_name = 'mk'
        rawdata = pd.read_excel(data_path, sheet_name=sheet_name)
        project = cls.__case_data(rawdata)
        return project

    @classmethod
    def __case_data(cls, rawdata):
        temp = rawdata.T.reset_index()
        user_attr = temp.iloc[0:2, 0:6]
        user_attr.columns = user_attr.iloc[0]
        user_attr = user_attr.iloc[1]
        return Project(
            data=cls.__get_data(rawdata),
            code=user_attr[0],
            project_name=user_attr[1],
            programme=user_attr[2],
            start_date=user_attr[3],
            version=user_attr[4],
            made_by=user_attr[5])

    @classmethod
    def __get_data(cls, rawdata):
        df = rawdata.iloc[6:]
        df_2 = df.iloc[0]
        columns_categorical = ['type_1', 'type_2', 'type_3', 'dzo']
        # columns_dates = df.iloc[,4:]
        # self.rawdata
        return df_2

    @classmethod
    def prepare_for_calculation(self):
        pass


class Calculator:

    @classmethod
    def calculate(cls, calculation):
        pass
        # return Result(...)


project = ProjectFactory.from_excel(PATH)
calculation = ProjectCalculationAdapter(project).get_calculation(effect_types=[EffectType.DMV, EffectType.UMV])

result = Calculator.calculate(calculation)

if __name__ == '__main__':
    case = ProjectFactory.from_excel(PATH)

    print()
    print(case.code)
