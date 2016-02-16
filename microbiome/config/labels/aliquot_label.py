from lis.labeling.classes import ZplTemplateTuple

"""Added here to override the default in app_configuration."""

aliquot_label = ZplTemplateTuple(
    'aliquot_label', (
        ('^XA\n'
         '~SD22'
         '^FO310,15^A0N,20,20^FD${protocol} Site ${site} ${clinician_initials}   ${aliquot_type} ${aliquot_count}${primary}^FS\n'
         '^FO310,34^BY1,3.0^BCN,50,N,N,N\n'
         '^BY^FD${aliquot_identifier}^FS\n'
         '^FO315,92^A0N,20,20^FD${aliquot_identifier}^FS\n'
         '^FO310,112^A0N,20,20^FD${subject_identifier} (${initials})^FS\n'
         '^FO310,132^A0N,20,20^FDDOB: ${dob} ${gender}^FS\n'
         '^FO310,152^A0N,25,20^FD${drawn_datetime}^FS\n'
         '^XZ')
    ), True)
