import labkey
from DataModeling.DataModels import *
from DataLoadingGlobals import *


class Field:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.spans = []


def get_annotations_from_server():
    # type: () -> object
    context = labkey.utils.create_server_context(SERVER, PROJECT, use_ssl=True)

    all_fields = labkey.query.select_rows(
        server_context=context,
        schema_name='nlp',
        query_name='FieldResult'
    )

    all_offsets = labkey.query.select_rows(
        server_context=context,
        schema_name='nlp',
        query_name='startStopPosition'
    )

    reports = labkey.query.select_rows(
        server_context=context,
        schema_name='nlp',
        query_name='report'
    )

    fields_per_report = find_fields(all_fields, all_offsets)
    events_per_report = convert_to_report_substance_events(fields_per_report)
    patient_doc_annotations = match_reports_to_patients(events_per_report, reports)

    return patient_doc_annotations


def find_fields(all_fields, all_offsets):
    field_query_results = [f for f in all_fields[ROWS] if (f[u'TargetTable'] == SOC_HISTORIES)]
    fields, field_names_per_report = create_field_objects(field_query_results)
    add_field_offsets(fields, all_offsets)
    fields_per_report = find_fields_per_report(fields, field_names_per_report)
    return fields_per_report


def create_field_objects(field_data):
    fields = {}                 # {field_id: Field}
    fields_per_report = {}      # {report_id: [field_id]}
    for field in field_data:
        field_id = field[FIELD_ID]
        field_obj = Field(field[FIELD_NAME], field[VALUE])

        fields[field_id] = field_obj
        update_fields_per_report(field, field_id, fields_per_report)

    return fields, fields_per_report


def update_fields_per_report(field, field_id, fields_per_report):
    report_id = field[REPORT_ID]
    if report_id not in fields_per_report:
        fields_per_report[report_id] = []
    fields_per_report[report_id].append(field_id)


def add_field_offsets(fields, all_offsets):
    for offset in all_offsets[ROWS]:
        field_id = offset[FIELD_ID]
        if field_id in fields:
            span = Span(offset[START_POS], offset[STOP_POS])
            fields[field_id].spans.append(span)


def find_fields_per_report(fields, field_names_per_report):
    fields_per_report = {}  # {report_id: [Field objects]}
    for report_id in field_names_per_report:
        fields_per_report[report_id] = []

        for field_id in field_names_per_report[report_id]:
            fields_per_report[report_id].append(fields[field_id])

    return fields_per_report


def convert_to_report_substance_events(fields_per_report):
    field_names_per_subst = find_substance_field_names()

    events_per_report = {}
    for report_id in fields_per_report:
        events_per_report[report_id] = create_events()

        fields = fields_per_report[report_id]
        for field in fields:
            for substance in SUBSTANCE_TYPES:
                if field.name in field_names_per_subst[substance]:
                    add_field_to_event(field, substance, events_per_report[report_id][substance])
                    break

    return events_per_report


def find_substance_field_names():
    """Find the set of LabKey field names for each substance type"""
    fields_per_subst = {}
    for subst in SUBSTANCE_TYPES:
        # Status
        status = subst + STATUS
        fields_per_subst[subst] = {status}

        # Substance-specific attributes
        for attrib in ATTRIBS[subst]:
            attrib_label = subst + attrib
            fields_per_subst[subst].add(attrib_label)

    return fields_per_subst


def create_events():
    events = {}
    for substance in SUBSTANCE_TYPES:
        events[substance] = Event(substance)
    return events


def add_field_to_event(field, substance, event):
    # Get rid of "Alcohol", "Tobacco", etc
    field_name = field.name.lstrip(substance)

    if field_name == STATUS:
        event.status = field.value
    elif field_name in ATTRIBS[substance]:
        event.attributes[field_name] = field.value


def match_reports_to_patients(events_per_report, all_reports):
    doc_events_per_patient = {}
    for report in all_reports[ROWS]:
        report_id = report[REPORT_ID]

        if report_id in events_per_report:
            add_to_patient_doc_events(report, report_id, events_per_report, doc_events_per_patient)

    return doc_events_per_patient


def add_to_patient_doc_events(report, report_id, events_per_report, doc_events_per_patient):
    mrn = report[MRN]
    doc_id = report[DOC_ID]

    if mrn not in doc_events_per_patient:
        doc_events_per_patient[mrn] = {}

    doc_events_per_patient[mrn][doc_id] = events_per_report[report_id]


if __name__ == '__main__':
    annot = get_annotations_from_server()
    print(annot)
