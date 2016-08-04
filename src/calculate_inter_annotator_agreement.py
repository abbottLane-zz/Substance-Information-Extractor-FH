from DataLoading import ServerQuery, IAADataFiltering
from SystemUtilities.Globals import *


class FieldIAAInfo:
    """ Matrix information for Fleiss Kappa calculation """
    def __init__(self, rows, column_sums, occurrences=0):
        self.rows = rows
        self.column_sums = column_sums
        self.total = sum(column_sums)
        self.occurrences = occurrences


def main():
    all_annotations = ServerQuery.get_annotations_from_server()
    interannotated_docs, iaa_is_possible, num_of_annotators = IAADataFiltering.get_interannotated_docs(all_annotations)

    if iaa_is_possible:
        calculate_iaa(interannotated_docs, num_of_annotators)
    else:
        print("Cannot calculate IAA - No fully inter-annotated docs")


def calculate_iaa(annotations, num_of_annotators):
    """Use Fleiss Kappa for several annotator interrater agreement"""
    value_infos, highlight_infos = field_iaa_info(annotations)

    # kappa for each individual field
    for subst in SUBSTANCE_TYPES:
        print("\n" + subst)
        fields = [STATUS] + ATTRIBS[subst]
        for field in fields:
            value_kappa = find_iaa([value_infos[subst][field]], num_of_annotators)
            span_kappa = find_iaa([highlight_infos[subst][field]], num_of_annotators)
            print(field + " value: " + str(value_kappa))
            print("\t\tspans: " + str(span_kappa))

    # Event Detection/ Status Classification (status info highlighting + field values)
    # status_list = [value_infos[subst][STATUS] for subst in SUBSTANCE_TYPES]
    # status_value_kappa = find_iaa(status_list, num_of_annotators)

    # Attribute Extraction (attribute field highlighting)

    # Attribute value selection (attribute field value)

    # Total (field values) -- Append columns together


def field_iaa_info(annotations):
    value_field_infos = {subst: {} for subst in SUBSTANCE_TYPES}
    highlight_field_infos = {subst: {} for subst in SUBSTANCE_TYPES}

    for substance in SUBSTANCE_TYPES:
        for field in FIELDS:
            # value IAA
            value_field_infos[substance][field] = get_single_field_info(annotations, substance, field)

            # highlighted regions IAA
            highlight_field_infos[substance][field] = get_single_field_info(annotations, substance, field,
                                                                            spans_instead_of_value=True)

    return value_field_infos, highlight_field_infos


def get_single_field_info(annotations, substance, field, spans_instead_of_value=False):
    if spans_instead_of_value:
        field = get_single_field_spans_info(annotations, substance, field)
    else:
        field = get_single_field_value_info(annotations, substance, field)

    return field


def get_single_field_value_info(annotations, substance, field):
    """ Track matrix of inter-annotated values for a field """
    column_value_map = {}   # {value: column number}
    column_map_index = 0
    column_sums = []
    rows = []
    occurrences = 0

    for doc_id in annotations:
        row = [0 for _ in column_value_map]

        for annotator in annotations[doc_id]:
            event = annotations[doc_id][annotator][substance]
            value = get_field_value(event, field)

            # Keep track of non-blank values
            if value:
                occurrences += 1

            # update rows and columns
            if value not in column_value_map:
                row.append(1)
                column_sums.append(1)
                column_value_map[value] = column_map_index
                column_map_index += 1
            else:
                column = column_value_map[value]
                row[column] += 1
                column_sums[column] += 1

        rows.append(row)

    return FieldIAAInfo(rows, column_sums, occurrences)


def get_single_field_spans_info(annotations, substance, field):
    """ Track matrix of inter-annotated spans for a field """
    # Track matrix of annotated values
    column_value_map = []  # [value] -- can't do dict bc lists of spans aren't hashable
    column_map_index = 0
    column_sums = []
    rows = []
    occurrences = 0

    for doc_id in annotations:
        row = [0 for _ in column_value_map]

        for annotator in annotations[doc_id]:
            event = annotations[doc_id][annotator][substance]
            value = get_field_spans(event, field)

            # Keep track of non-blank values
            if value:
                occurrences += 1

            value_in_map, column = check_if_exact_spans_in_map(column_value_map, value)

            # update rows and columns
            if not value_in_map:
                row.append(1)
                column_sums.append(1)
                column_value_map.append(value)
                column_map_index += 1
            else:
                row[column] += 1
                column_sums[column] += 1

        rows.append(row)

    return FieldIAAInfo(rows, column_sums, occurrences)


def check_if_exact_spans_in_map(seen_span_lists, span_list):
    previously_seen = False
    column_index = 0

    for column_index, seen_span_list in enumerate(seen_span_lists):
        total_match = spans_totally_match(seen_span_list, span_list)
        if total_match:
            previously_seen = True
            break

    return previously_seen, column_index


def spans_totally_match(seen_span_list, span_list):
    total_match = True

    if len(seen_span_list) != len(span_list):
        total_match = False
    else:
        for seen_span, span in zip(seen_span_list, span_list):
            if seen_span.start != span.start or seen_span.stop != span.stop:
                total_match = False
                break

    return total_match


def get_field_value(event, field):
    value = ""
    if field == STATUS:
        value = event.status
    elif field in event.attributes:
        value = event.attributes[field].text
    return value


def get_field_spans(event, field):
    value = ""
    if field == STATUS:
        value = event.status_spans
    elif field in event.attributes:
        value = event.attributes[field].spans
    return value


def find_iaa(list_of_field_infos, num_of_annotators):
    """ Fleiss kappa calculation using each field's matrix info in FieldIAAInfo objects """
    combined_info = combine_different_value_field_infos(list_of_field_infos)

    if combined_info.occurrences > 0:
        kappa = calculate_fleiss_kappa(combined_info, num_of_annotators)
    else:
        kappa = None

    return kappa


def combine_different_value_field_infos(list_of_field_infos):
    """ Simply append rows and columns together """
    rows = []
    column_sums = []
    occurrences = 0
    if list_of_field_infos:
        for field_index, field_info in enumerate(list_of_field_infos):
            rows.extend(field_info.rows)
            column_sums.extend(field_info.column_sums)
            occurrences += field_info.occurrences

    return FieldIAAInfo(rows, column_sums, occurrences)


def combine_same_value_field_infos(list_of_field_infos):
    """ append rows and sum columns together """
    rows = []
    column_sums = []
    occurrences = 0
    if list_of_field_infos:

        # Set column_sum to the column_sums of the first field
        column_sums = list_of_field_infos[0].column_sums
        for field_index, field_info in enumerate(list_of_field_infos):
            # Grab each row
            rows.extend(field_info.rows)
            occurrences += field_info.occurrences

            # Add all non-first column sums to the first one
            if field_index > 0:
                for column_index, column_sum in enumerate(field_info.column_sums):
                    column_sums[column_index] += column_sum

    return FieldIAAInfo(rows, column_sums, occurrences)


def calculate_fleiss_kappa(combined_info, num_of_annotators):
    # Find Pj for calculating Pe
    pj = [float(c) / float(combined_info.total) for c in combined_info.column_sums]
    expected_prob = sum([c ** 2 for c in pj])

    # Find Pi for calculating P
    pi = []
    for row in combined_info.rows:
        pi_coefficient = float(1) / float(num_of_annotators * (num_of_annotators - 1))
        pi_sum = sum([v ** 2 for v in row]) - num_of_annotators
        pi.append(pi_coefficient * pi_sum)

    observed_prob = float(sum(pi)) / float(len(pi))

    # Use P and Pe to calculate kappa
    if expected_prob != 1:
        kappa = float((observed_prob - expected_prob)) / float((1 - expected_prob))
    else:
        kappa = 1

    return kappa


if __name__ == '__main__':
    main()
