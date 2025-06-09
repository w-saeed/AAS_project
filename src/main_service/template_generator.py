import pandas as pd
from aas_core3 import types as aas
from aas_core3 import jsonization as aas_jsonization
import json

class TemplateGenerator:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    @staticmethod
    def create_linked_segment_value(id_short: str, name: str, description: str, record_count: str, sampling_interval: str, start_time: str, end_time: str, endpoint: str):

        segment_elements = [
            aas.MultiLanguageProperty(
                category="PARAMETER",
                id_short="Name",
                semantic_id=aas.Reference(
                    type=aas.ReferenceTypes.EXTERNAL_REFERENCE,
                    keys=[
                        aas.Key(
                            type=aas.KeyTypes.GLOBAL_REFERENCE,
                            value="https://admin-shell.io/idta/TimeSeries/Segment/Name/1/1"
                        )
                    ]
                ),
                value=[aas.LangStringNameType(language="en", text=name)]
            ),
            aas.MultiLanguageProperty(
                category="PARAMETER",
                id_short="Description",
                semantic_id=aas.Reference(
                    type=aas.ReferenceTypes.EXTERNAL_REFERENCE,
                    keys=[
                        aas.Key(
                            type=aas.KeyTypes.GLOBAL_REFERENCE,
                            value="https://admin-shell.io/idta/TimeSeries/Segment/Description/1/1"
                        )
                    ]
                ),
                value=[aas.LangStringNameType(language="en", text=description)]
            ),
            aas.Property(
                category="VARIABLE",
                id_short="RecordCount",
                semantic_id=aas.Reference(
                    type=aas.ReferenceTypes.EXTERNAL_REFERENCE,
                    keys=[
                        aas.Key(
                            type=aas.KeyTypes.GLOBAL_REFERENCE,
                            value="https://admin-shell.io/idta/TimeSeries/Segment/RecordCount/1/1"
                        )
                    ]
                ),
                value_type=aas.DataTypeDefXSD.STRING,
                value=record_count
            ),
            aas.Property(
                category="PARAMETER",
                id_short="SamplingInterval",
                semantic_id=aas.Reference(
                    type=aas.ReferenceTypes.EXTERNAL_REFERENCE,
                    keys=[
                        aas.Key(
                            type=aas.KeyTypes.GLOBAL_REFERENCE,
                            value="https://admin-shell.io/idta/TimeSeries/Segment/SamplingInterval/1/1"
                        )
                    ]
                ),
                value_type=aas.DataTypeDefXSD.STRING,
                value=sampling_interval
            ),
            aas.Property(
                category="VARIABLE",
                id_short="StartTime",
                semantic_id=aas.Reference(
                    type=aas.ReferenceTypes.EXTERNAL_REFERENCE,
                    keys=[
                        aas.Key(
                            type=aas.KeyTypes.GLOBAL_REFERENCE,
                            value="https://admin-shell.io/idta/TimeSeries/Segment/StartTime/1/1"
                        )
                    ]
                ),
                value_type=aas.DataTypeDefXSD.STRING,
                value=start_time
            ),
            aas.Property(
                category="VARIABLE",
                id_short="EndTime",
                semantic_id=aas.Reference(
                    type=aas.ReferenceTypes.EXTERNAL_REFERENCE,
                    keys=[
                        aas.Key(
                            type=aas.KeyTypes.GLOBAL_REFERENCE,
                            value="https://admin-shell.io/idta/TimeSeries/Segment/EndTime/1/1"
                        )
                    ]
                ),
                value_type=aas.DataTypeDefXSD.STRING,
                value=end_time
            ),
            aas.Property(
                category="PARAMETER",
                id_short="Endpoint",
                semantic_id=aas.Reference(
                    type=aas.ReferenceTypes.EXTERNAL_REFERENCE,
                    keys=[
                        aas.Key(
                            type=aas.KeyTypes.GLOBAL_REFERENCE,
                            value="https://admin-shell.io/idta/TimeSeries/Endpoint/1/1"
                        )
                    ]
                ),
                value_type=aas.DataTypeDefXSD.STRING,
                value=endpoint
            )
        ]

        linked_segment = aas.SubmodelElementCollection(
            id_short=id_short,
            semantic_id=aas.Reference(
                type=aas.ReferenceTypes.EXTERNAL_REFERENCE,
                keys=[
                    aas.Key(
                        type=aas.KeyTypes.GLOBAL_REFERENCE,
                        value="https://admin-shell.io/idta/TimeSeries/Segments/LinkedSegment/1/1"
                    )
                ]
            ),
            qualifiers=[
                aas.Qualifier(
                    type="Cardinality",
                    value_type=aas.DataTypeDefXSD.STRING,
                    value="ZeroToMany"
                )
            ],
            value=segment_elements
        )
        return linked_segment

    def build_segments_json(self):
        """
        Iterates the DataFrame and creates a list of JSON-serializable linked segment elements.
        """
        segment_json_list = []
        for _, row in self.df.iterrows():
            seg = self.create_linked_segment_value(
                id_short=row["sensor_id"],
                name=row["sensor_id"],
                description=f'{row["sensor_id"]} is responsible for measuring {row["measurement_type"]}',
                record_count=str(row["record_count"]),
                sampling_interval=str(row["sampling_interval"]),
                start_time=row["start_time"],
                end_time=row["end_time"],
                endpoint=f'http://localhost:8000/api/v1/aas/assetid/submodels/time-series/{row["sensor_id"]}/min'
            )
            seg_json = aas_jsonization.to_jsonable(seg)
            segment_json_list.append(seg_json)
        return segment_json_list


