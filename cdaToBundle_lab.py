
import sys
import argparse
import time
import uuid
import builtins
import re
import io
import json
from datetime import datetime
import dateutil.parser
from html import escape as html_escape
import malac.models.cda.at_ext
import malac.models.fhir.r4
from malac.models.fhir.r4 import string, base64Binary, markdown, code, dateTime, uri, boolean, decimal
from malac.models.fhir import utils
from malac.utils import fhirpath

description_text = "This has been compiled by the MApping LAnguage compiler for Health Data, short MaLaC-HD. See arguments for more details."
one_timestamp = datetime.now()
fhirpath_utils = fhirpath.FHIRPathUtils(malac.models.fhir.r4)
shared_vars = {}

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description_text)
    parser.add_argument(
       '-s', '--source', help='the source file path', required=True
    )
    parser.add_argument(
       '-t', '--target', help='the target file path the result will be written to', required=True
    )
    return parser

def transform(source_path, target_path):
    start = time.time()
    print('+++++++ Transformation from '+source_path+' to '+target_path+' started +++++++')

    if source_path.endswith('.xml'):
        cda = malac.models.cda.at_ext.parse(source_path, silence=True)
    else:
        raise BaseException('Unknown source file ending: ' + source_path)
    fhir_bundle = malac.models.fhir.r4.Bundle()
    CdaToFhirBundle(cda, fhir_bundle)
    with open(target_path, 'w', newline='', encoding='utf-8') as f:
        if target_path.endswith('.xml'):
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            fhir_bundle.export(f, 0, namespacedef_='xmlns="http://hl7.org/fhir" xmlns:v3="urn:hl7-org:v3"')
        elif target_path.endswith('.json'):
            json.dump(fhir_bundle.exportJson(), f)
        else:
            raise BaseException('Unknown target file ending')

    print('altogether in '+str(round(time.time()-start,3))+' seconds.')
    print('+++++++ Transformation from '+source_path+' to '+target_path+' ended  +++++++')

def CdaToFhirBundle(cda, fhir_bundle):
    fhir_bundle.id = string(value=str(uuid.uuid4()))
    fhir_bundle.type_ = string(value='document')
    fhir_bundle_meta = malac.models.fhir.r4.Meta()
    if fhir_bundle.meta is not None:
        fhir_bundle_meta = fhir_bundle.meta
    else:
        fhir_bundle.meta = fhir_bundle_meta
    fhir_bundle_meta.profile.append(string(value='http://hl7.eu/fhir/laboratory/StructureDefinition/Bundle-eu-lab'))
    if cda.id:
        fhir_bundle.identifier = malac.models.fhir.r4.Identifier()
        II(cda.id, fhir_bundle.identifier)
    if cda.effectiveTime:
        fhir_bundle.timestamp = malac.models.fhir.r4.instant()
        TSInstant(cda.effectiveTime, fhir_bundle.timestamp)
    fhir_bundle_entry_1 = malac.models.fhir.r4.Bundle_Entry()
    fhir_bundle.entry.append(fhir_bundle_entry_1)
    fhir_composition = malac.models.fhir.r4.Composition()
    fhir_bundle_entry_1.resource = malac.models.fhir.r4.ResourceContainer(Composition=fhir_composition)
    fhir_composition_uuid = string(value=str(uuid.uuid4()))
    fhir_composition.id = fhir_composition_uuid
    fhir_bundle_entry_1.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_composition_uuid is None else fhir_composition_uuid if isinstance(fhir_composition_uuid, str) else fhir_composition_uuid.value)))
    fhir_bundle_entry_4 = malac.models.fhir.r4.Bundle_Entry()
    fhir_bundle.entry.append(fhir_bundle_entry_4)
    fhir_diagnosticReport = malac.models.fhir.r4.DiagnosticReport()
    fhir_bundle_entry_4.resource = malac.models.fhir.r4.ResourceContainer(DiagnosticReport=fhir_diagnosticReport)
    fhir_diagnosticReport_id = string(value=str(uuid.uuid4()))
    fhir_diagnosticReport.id = fhir_diagnosticReport_id
    fhir_bundle_entry_4.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_diagnosticReport_id is None else fhir_diagnosticReport_id if isinstance(fhir_diagnosticReport_id, str) else fhir_diagnosticReport_id.value)))
    fhir_bundle_entry_2 = malac.models.fhir.r4.Bundle_Entry()
    fhir_bundle.entry.append(fhir_bundle_entry_2)
    fhir_patient = malac.models.fhir.r4.Patient()
    fhir_bundle_entry_2.resource = malac.models.fhir.r4.ResourceContainer(Patient=fhir_patient)
    fhir_patient_uuid = string(value=str(uuid.uuid4()))
    fhir_patient.id = fhir_patient_uuid
    fhir_bundle_entry_2.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_patient_uuid is None else fhir_patient_uuid if isinstance(fhir_patient_uuid, str) else fhir_patient_uuid.value)))
    fhir_bundle_entry_5 = malac.models.fhir.r4.Bundle_Entry()
    fhir_bundle.entry.append(fhir_bundle_entry_5)
    fhir_serviceRequest = malac.models.fhir.r4.ServiceRequest()
    fhir_bundle_entry_5.resource = malac.models.fhir.r4.ResourceContainer(ServiceRequest=fhir_serviceRequest)
    fhir_serviceRequest_id = string(value=str(uuid.uuid4()))
    fhir_serviceRequest.id = fhir_serviceRequest_id
    fhir_bundle_entry_5.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_serviceRequest_id is None else fhir_serviceRequest_id if isinstance(fhir_serviceRequest_id, str) else fhir_serviceRequest_id.value)))
    fhir_serviceRequest_meta = malac.models.fhir.r4.Meta()
    if fhir_serviceRequest.meta is not None:
        fhir_serviceRequest_meta = fhir_serviceRequest.meta
    else:
        fhir_serviceRequest.meta = fhir_serviceRequest_meta
    fhir_serviceRequest_meta.profile.append(string(value='http://hl7.eu/fhir/laboratory/StructureDefinition/ServiceRequest-eu-lab'))
    fhir_composition_extenstion_01 = malac.models.fhir.r4.Extension()
    fhir_composition.extension.append(fhir_composition_extenstion_01)
    fhir_composition_extenstion_01.url = 'http://hl7.eu/fhir/StructureDefinition/composition-basedOn-order-or-requisition'
    fhir_diagnosticReport_composition_reference = malac.models.fhir.r4.Reference()
    fhir_composition_extenstion_01.valueReference = fhir_diagnosticReport_composition_reference
    fhir_diagnosticReport_composition_reference.reference = string(value=('urn:uuid:' + ('' if fhir_serviceRequest_id is None else fhir_serviceRequest_id if isinstance(fhir_serviceRequest_id, str) else fhir_serviceRequest_id.value)))
    fhir_diagnosticReport_composition_reference.type_ = uri(value='ServiceRequest')
    fhir_composition_subject_reference = malac.models.fhir.r4.Reference()
    fhir_composition.subject = fhir_composition_subject_reference
    fhir_composition_subject_reference.reference = string(value=('urn:uuid:' + ('' if fhir_patient_uuid is None else fhir_patient_uuid if isinstance(fhir_patient_uuid, str) else fhir_patient_uuid.value)))
    fhir_composition_subject_reference.type_ = uri(value='Patient')
    fhir_composition_extenstion_02 = malac.models.fhir.r4.Extension()
    fhir_composition.extension.append(fhir_composition_extenstion_02)
    fhir_composition_extenstion_02.url = 'http://hl7.eu/fhir/laboratory/StructureDefinition/composition-diagnosticReportReference'
    fhir_composition_diagnosticReport_reference = malac.models.fhir.r4.Reference()
    fhir_composition_extenstion_02.valueReference = fhir_composition_diagnosticReport_reference
    fhir_composition_diagnosticReport_reference.reference = string(value=('urn:uuid:' + ('' if fhir_diagnosticReport_id is None else fhir_diagnosticReport_id if isinstance(fhir_diagnosticReport_id, str) else fhir_diagnosticReport_id.value)))
    fhir_composition_diagnosticReport_reference.type_ = uri(value='DiagnosticReport')
    fhir_diagnosticReport_extension = malac.models.fhir.r4.Extension()
    fhir_diagnosticReport.extension.append(fhir_diagnosticReport_extension)
    fhir_diagnosticReport_extension.url = 'http://hl7.org/fhir/5.0/StructureDefinition/extension-DiagnosticReport.composition'
    fhir_diagnosticReport_composition_reference = malac.models.fhir.r4.Reference()
    fhir_diagnosticReport_extension.valueReference = fhir_diagnosticReport_composition_reference
    fhir_diagnosticReport_composition_reference.reference = string(value=('urn:uuid:' + ('' if fhir_composition_uuid is None else fhir_composition_uuid if isinstance(fhir_composition_uuid, str) else fhir_composition_uuid.value)))
    fhir_diagnosticReport_composition_reference.type_ = uri(value='Composition')
    fhir_diagnosticReport_basedOn_reference = malac.models.fhir.r4.Reference()
    fhir_diagnosticReport.basedOn.append(fhir_diagnosticReport_basedOn_reference)
    fhir_diagnosticReport_basedOn_reference.reference = string(value=('urn:uuid:' + ('' if fhir_serviceRequest_id is None else fhir_serviceRequest_id if isinstance(fhir_serviceRequest_id, str) else fhir_serviceRequest_id.value)))
    fhir_diagnosticReport_basedOn_reference.type_ = uri(value='ServiceRequest')
    fhir_diagnosticReport_subject_reference = malac.models.fhir.r4.Reference()
    fhir_diagnosticReport.subject = fhir_diagnosticReport_subject_reference
    fhir_diagnosticReport_subject_reference.reference = string(value=('urn:uuid:' + ('' if fhir_patient_uuid is None else fhir_patient_uuid if isinstance(fhir_patient_uuid, str) else fhir_patient_uuid.value)))
    fhir_diagnosticReport_subject_reference.type_ = uri(value='Patient')
    fhir_serviceRequest_subject_reference = malac.models.fhir.r4.Reference()
    fhir_serviceRequest.subject = fhir_serviceRequest_subject_reference
    fhir_serviceRequest_subject_reference.reference = string(value=('urn:uuid:' + ('' if fhir_patient_uuid is None else fhir_patient_uuid if isinstance(fhir_patient_uuid, str) else fhir_patient_uuid.value)))
    fhir_serviceRequest_subject_reference.type_ = uri(value='Patient')
    fhir_bundle_entry01 = malac.models.fhir.r4.Bundle_Entry()
    fhir_bundle.entry.append(fhir_bundle_entry01)
    fhir_practitionerRole = malac.models.fhir.r4.PractitionerRole()
    fhir_bundle_entry01.resource = malac.models.fhir.r4.ResourceContainer(PractitionerRole=fhir_practitionerRole)
    fhir_practitionerRole_id = string(value=str(uuid.uuid4()))
    fhir_practitionerRole.id = fhir_practitionerRole_id
    fhir_bundle_entry01.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_practitionerRole_id is None else fhir_practitionerRole_id if isinstance(fhir_practitionerRole_id, str) else fhir_practitionerRole_id.value)))
    CdaHeaderToFhirComposition(cda, fhir_composition, fhir_patient, fhir_diagnosticReport, fhir_serviceRequest, fhir_bundle)
    CdaHeaderToFhirDiagnosticReport(cda, fhir_diagnosticReport)
    cda_component = cda.component
    if cda_component:
        cda_structuredBody = cda_component.structuredBody
        if cda_structuredBody:
            CdaToPractitionerRole(cda, fhir_practitionerRole, fhir_bundle)
            CdaBodyToFhirComposition(cda, cda_structuredBody, fhir_composition, fhir_practitionerRole, fhir_patient, fhir_diagnosticReport, fhir_bundle)

def CdaHeaderToFhirComposition(cda, fhir_composition, fhir_patient, fhir_diagnosticReport, fhir_serviceRequest, fhir_bundle):
    fhir_composition_meta = malac.models.fhir.r4.Meta()
    if fhir_composition.meta is not None:
        fhir_composition_meta = fhir_composition.meta
    else:
        fhir_composition.meta = fhir_composition_meta
    fhir_composition_meta.profile.append(string(value='http://hl7.eu/fhir/laboratory/StructureDefinition/Composition-eu-lab'))
    cda_code = cda.code
    if cda_code:
        code_code = cda_code.code
        if code_code:
            fhir_composition_category = malac.models.fhir.r4.CodeableConcept()
            fhir_composition.category.append(fhir_composition_category)
            fhir_composition_category.coding.append(translate_single('cda-code-2-fhir-category', (code_code if isinstance(code_code, str) else code_code.value), 'Coding'))
    cda_code = cda.code
    if cda_code:
        for translation in cda_code.translation or []:
            fhir_composition.type_ = malac.models.fhir.r4.CodeableConcept()
            CDCodeableConcept(translation, fhir_composition.type_)
        if fhirpath.single(fhirpath_utils.bool_not([bool([v2 for v1 in [cda_code] for v2 in fhirpath_utils.get(v1,'translation')])])):
            type_coding = malac.models.fhir.r4.CodeableConcept()
            fhir_composition.type_ = type_coding
            coding_coding = malac.models.fhir.r4.Coding()
            type_coding.coding.append(coding_coding)
            coding_coding.system = uri(value='http://loinc.org')
            coding_coding.code = string(value='11502-2')
    cda_title = cda.title
    if cda_title:
        fhir_composition.title = string(value=fhirpath.single([v2 for v1 in [cda_title] for v2 in fhirpath_utils.get(v1,'valueOf_',strip=True)]))
    cda_statusCode = cda.statusCode
    if cda_statusCode:
        if fhirpath.single([bool([v2 for v1 in [cda] for v2 in fhirpath_utils.get(v1,'sdtcStatusCode')])]):
            cda_code = cda_statusCode.code
            if cda_code:
                fhir_composition.status = string(value=translate_single('cda-sdtc-statuscode-2-fhir-composition-status', (cda_code if isinstance(cda_code, str) else cda_code.value), 'code'))
    if fhirpath.single(fhirpath_utils.bool_not([bool([v2 for v1 in [cda] for v2 in fhirpath_utils.get(v1,'sdtcStatusCode')])])):
        fhir_composition.status = string(value='final')
    if cda.effectiveTime:
        fhir_composition.date = malac.models.fhir.r4.dateTime()
        TSDateTime(cda.effectiveTime, fhir_composition.date)
    if cda.confidentialityCode:
        fhir_composition.confidentiality = malac.models.fhir.r4.Confidentiality()
        transform_default(cda.confidentialityCode, fhir_composition.confidentiality, malac.models.fhir.r4.code)
    if cda.languageCode:
        fhir_composition.language = malac.models.fhir.r4.code()
        transform_default(cda.languageCode, fhir_composition.language)
    if cda.setId:
        fhir_composition.identifier = malac.models.fhir.r4.Identifier()
        II(cda.setId, fhir_composition.identifier)
    cda_versionNumber = cda.versionNumber
    if cda_versionNumber:
        cda_versionNumber_value = cda_versionNumber.value
        if cda_versionNumber_value:
            fhir_composition_extenstion = malac.models.fhir.r4.Extension()
            fhir_composition.extension.append(fhir_composition_extenstion)
            fhir_composition_extenstion.url = 'http://hl7.org/fhir/StructureDefinition/composition-clinicaldocument-versionNumber'
            fhir_composition_extenstion.valueString = string(value=str(cda_versionNumber_value))
    for cda_recordTarget in cda.recordTarget or []:
        cda_patientRole = cda_recordTarget.patientRole
        if cda_patientRole:
            CdaPatientRoleToFhirPatient(cda_patientRole, fhir_patient, fhir_bundle)
    for cda_author in cda.author or []:
        if fhirpath.single([bool([v4 for v3 in [v2 for v1 in [cda_author] for v2 in fhirpath_utils.get(v1,'assignedAuthor')] for v4 in fhirpath_utils.get(v3,'assignedPerson')])]):
            fhir_bundle_entry = malac.models.fhir.r4.Bundle_Entry()
            fhir_bundle.entry.append(fhir_bundle_entry)
            fhir_practitionerRole = malac.models.fhir.r4.PractitionerRole()
            fhir_bundle_entry.resource = malac.models.fhir.r4.ResourceContainer(PractitionerRole=fhir_practitionerRole)
            fhir_practitionerRole_id = string(value=str(uuid.uuid4()))
            fhir_practitionerRole.id = fhir_practitionerRole_id
            fhir_bundle_entry.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_practitionerRole_id is None else fhir_practitionerRole_id if isinstance(fhir_practitionerRole_id, str) else fhir_practitionerRole_id.value)))
            fhir_composition_author_reference = malac.models.fhir.r4.Reference()
            fhir_composition.author.append(fhir_composition_author_reference)
            fhir_composition_author_reference.reference = string(value=('urn:uuid:' + ('' if fhir_practitionerRole_id is None else fhir_practitionerRole_id if isinstance(fhir_practitionerRole_id, str) else fhir_practitionerRole_id.value)))
            fhir_composition_author_reference.type_ = uri(value='PractitionerRole')
            CdaAuthorToFhirPractitionerRole(cda_author, fhir_practitionerRole, fhir_bundle)
    for cda_author in cda.author or []:
        if fhirpath.single([bool([v4 for v3 in [v2 for v1 in [cda_author] for v2 in fhirpath_utils.get(v1,'assignedAuthor')] for v4 in fhirpath_utils.get(v3,'assignedAuthoringDevice')])]):
            fhir_bundle_entry = malac.models.fhir.r4.Bundle_Entry()
            fhir_bundle.entry.append(fhir_bundle_entry)
            fhir_device = malac.models.fhir.r4.Device()
            fhir_bundle_entry.resource = malac.models.fhir.r4.ResourceContainer(Device=fhir_device)
            fhir_device_id = string(value=str(uuid.uuid4()))
            fhir_device.id = fhir_device_id
            fhir_bundle_entry.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_device_id is None else fhir_device_id if isinstance(fhir_device_id, str) else fhir_device_id.value)))
            fhir_composition_author_reference = malac.models.fhir.r4.Reference()
            fhir_composition.author.append(fhir_composition_author_reference)
            fhir_composition_author_reference.reference = string(value=('urn:uuid:' + ('' if fhir_device_id is None else fhir_device_id if isinstance(fhir_device_id, str) else fhir_device_id.value)))
            fhir_composition_author_reference.type_ = uri(value='Device')
            CdaAuthorToFhirDevice(cda_author, fhir_device, fhir_bundle)
    cda_custodian = cda.custodian
    if cda_custodian:
        cda_assignedCustodian = cda_custodian.assignedCustodian
        if cda_assignedCustodian:
            cda_representedCustodianOrganization = cda_assignedCustodian.representedCustodianOrganization
            if cda_representedCustodianOrganization:
                fhir_bundle_entry = malac.models.fhir.r4.Bundle_Entry()
                fhir_bundle.entry.append(fhir_bundle_entry)
                fhir_custodian_organization = malac.models.fhir.r4.Organization()
                fhir_bundle_entry.resource = malac.models.fhir.r4.ResourceContainer(Organization=fhir_custodian_organization)
                fhir_custodian_organization_id = string(value=str(uuid.uuid4()))
                fhir_custodian_organization.id = fhir_custodian_organization_id
                fhir_bundle_entry.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_custodian_organization_id is None else fhir_custodian_organization_id if isinstance(fhir_custodian_organization_id, str) else fhir_custodian_organization_id.value)))
                fhir_composition_custodian_reference = malac.models.fhir.r4.Reference()
                fhir_composition.custodian = fhir_composition_custodian_reference
                fhir_composition_custodian_reference.reference = string(value=('urn:uuid:' + ('' if fhir_custodian_organization_id is None else fhir_custodian_organization_id if isinstance(fhir_custodian_organization_id, str) else fhir_custodian_organization_id.value)))
                fhir_composition_custodian_reference.type_ = uri(value='Organization')
                for id_ in cda_representedCustodianOrganization.id or []:
                    fhir_custodian_organization.identifier.append(malac.models.fhir.r4.Identifier())
                    II(id_, fhir_custodian_organization.identifier[-1])
                if cda_representedCustodianOrganization.name:
                    fhir_custodian_organization.name = malac.models.fhir.r4.string()
                    transform_default(cda_representedCustodianOrganization.name, fhir_custodian_organization.name)
                for telecom in cda_representedCustodianOrganization.telecom or []:
                    fhir_custodian_organization.telecom.append(malac.models.fhir.r4.ContactPoint())
                    TELContactPoint(telecom, fhir_custodian_organization.telecom[-1])
                if cda_representedCustodianOrganization.addr:
                    fhir_custodian_organization.address.append(malac.models.fhir.r4.Address())
                    CdaAdressCompilationToFhirAustrianAddress(cda_representedCustodianOrganization.addr, fhir_custodian_organization.address[-1])
    for cda_legalAuthenticator in cda.legalAuthenticator or []:
        fhir_composition_attester = malac.models.fhir.r4.Composition_Attester()
        fhir_composition.attester.append(fhir_composition_attester)
        if cda_legalAuthenticator.time:
            fhir_composition_attester.time = malac.models.fhir.r4.dateTime()
            TSDateTime(cda_legalAuthenticator.time, fhir_composition_attester.time)
        fhir_composition_attester_mode = malac.models.fhir.r4.CompositionAttestationMode()
        if fhir_composition_attester.mode is not None:
            fhir_composition_attester_mode = fhir_composition_attester.mode
        else:
            fhir_composition_attester.mode = fhir_composition_attester_mode
        fhir_composition_attester_mode.codeString = string(value='legal')
        cda_legalAuthenticator_assignedEntity = cda_legalAuthenticator.assignedEntity
        if cda_legalAuthenticator_assignedEntity:
            fhir_bundle_entry01 = malac.models.fhir.r4.Bundle_Entry()
            fhir_bundle.entry.append(fhir_bundle_entry01)
            fhir_practitionerRole = malac.models.fhir.r4.PractitionerRole()
            fhir_bundle_entry01.resource = malac.models.fhir.r4.ResourceContainer(PractitionerRole=fhir_practitionerRole)
            fhir_practitionerRole_id = string(value=str(uuid.uuid4()))
            fhir_practitionerRole.id = fhir_practitionerRole_id
            fhir_bundle_entry01.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_practitionerRole_id is None else fhir_practitionerRole_id if isinstance(fhir_practitionerRole_id, str) else fhir_practitionerRole_id.value)))
            fhir_composition_attester_reference = malac.models.fhir.r4.Reference()
            fhir_composition_attester.party = fhir_composition_attester_reference
            fhir_composition_attester_reference.reference = string(value=('urn:uuid:' + ('' if fhir_practitionerRole_id is None else fhir_practitionerRole_id if isinstance(fhir_practitionerRole_id, str) else fhir_practitionerRole_id.value)))
            fhir_composition_attester_reference.type_ = uri(value='PractitionerRole')
            CdaAssignedEntityToFhirPractitionerRole(cda_legalAuthenticator_assignedEntity, fhir_practitionerRole, fhir_bundle)
    for cda_orderingProvider in cda.participant or []:
        if fhirpath.single(fhirpath_utils.equals([v2 for v1 in [cda_orderingProvider] for v2 in fhirpath_utils.get(v1,'typeCode')], '==', ['REF'])):
            fhir_bundle_entry = malac.models.fhir.r4.Bundle_Entry()
            fhir_bundle.entry.append(fhir_bundle_entry)
            fhir_practitionerRole = malac.models.fhir.r4.PractitionerRole()
            fhir_bundle_entry.resource = malac.models.fhir.r4.ResourceContainer(PractitionerRole=fhir_practitionerRole)
            fhir_practitionerRole_id = string(value=str(uuid.uuid4()))
            fhir_practitionerRole.id = fhir_practitionerRole_id
            fhir_bundle_entry.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_practitionerRole_id is None else fhir_practitionerRole_id if isinstance(fhir_practitionerRole_id, str) else fhir_practitionerRole_id.value)))
            fhir_serviceRequest_requester_reference = malac.models.fhir.r4.Reference()
            fhir_serviceRequest.requester = fhir_serviceRequest_requester_reference
            fhir_serviceRequest_requester_reference.reference = string(value=('urn:uuid:' + ('' if fhir_practitionerRole_id is None else fhir_practitionerRole_id if isinstance(fhir_practitionerRole_id, str) else fhir_practitionerRole_id.value)))
            fhir_serviceRequest_requester_reference.type_ = uri(value='PractitionerRole')
            cda_orderingProvider_time = cda_orderingProvider.time
            if cda_orderingProvider_time:
                v = cda_orderingProvider_time.value
                if v:
                    fhir_serviceRequest.authoredOn = dateTime(value=dateutil.parser.parse(v).isoformat())
            cda_associatedEntity = cda_orderingProvider.associatedEntity
            if cda_associatedEntity:
                CdaAssociatedEntityToFhirPractitionerRole(cda_associatedEntity, fhir_practitionerRole, fhir_bundle)
    for cda_inFulFillmentOf in cda.inFulfillmentOf or []:
        cda_inFulFillmentOf_order = cda_inFulFillmentOf.order
        if cda_inFulFillmentOf_order:
            for id__ in cda_inFulFillmentOf_order.id or []:
                fhir_serviceRequest.identifier.append(malac.models.fhir.r4.Identifier())
                II(id__, fhir_serviceRequest.identifier[-1])
            fhir_serviceRequest.status = string(value='completed')
            fhir_serviceRequest.intent = string(value='order')
    for cda_documentationOf in cda.documentationOf or []:
        cda_documentationOf_serviceEvent = cda_documentationOf.serviceEvent
        if cda_documentationOf_serviceEvent:
            fhir_composition_event = malac.models.fhir.r4.Composition_Event()
            fhir_composition.event.append(fhir_composition_event)
            for serviceEvent_id in cda_documentationOf_serviceEvent.id or []:
                serviceEvent_id_root = serviceEvent_id.root
                if serviceEvent_id_root:
                    event_codeableConcept = malac.models.fhir.r4.CodeableConcept()
                    fhir_composition_event.code.append(event_codeableConcept)
                    event_codeableConcept.text = string(value='serviceEvent-id')
                    event_codeableConcept_coding = malac.models.fhir.r4.Coding()
                    event_codeableConcept.coding.append(event_codeableConcept_coding)
                    event_codeableConcept_coding.code = string(value=serviceEvent_id_root)
            if cda_documentationOf_serviceEvent.code:
                fhir_composition_event.code.append(malac.models.fhir.r4.CodeableConcept())
                transform_default(cda_documentationOf_serviceEvent.code, fhir_composition_event.code[-1])
            if cda_documentationOf_serviceEvent.effectiveTime:
                fhir_composition_event.period = malac.models.fhir.r4.Period()
                IVLTSPeriod(cda_documentationOf_serviceEvent.effectiveTime, fhir_composition_event.period)
    for cda_relatedDocument in cda.relatedDocument or []:
        cda_parentDocument = cda_relatedDocument.parentDocument
        if cda_parentDocument:
            fhir_composition_relatesTo = malac.models.fhir.r4.Composition_RelatesTo()
            fhir_composition.relatesTo.append(fhir_composition_relatesTo)
            fhir_composition_relatesTo.code = string(value='replaces')
            for cda_parentDocument_id in cda_parentDocument.id or []:
                fhir_target_identifier = malac.models.fhir.r4.Identifier()
                fhir_composition_relatesTo.targetIdentifier = fhir_target_identifier
                II(cda_parentDocument_id, fhir_target_identifier)
    cda_componentOf = cda.componentOf
    if cda_componentOf:
        cda_encompassingEncounter = cda_componentOf.encompassingEncounter
        if cda_encompassingEncounter:
            fhir_bundle_entry = malac.models.fhir.r4.Bundle_Entry()
            fhir_bundle.entry.append(fhir_bundle_entry)
            fhir_encounter = malac.models.fhir.r4.Encounter()
            fhir_bundle_entry.resource = malac.models.fhir.r4.ResourceContainer(Encounter=fhir_encounter)
            fhir_encounter_id = string(value=str(uuid.uuid4()))
            fhir_encounter.id = fhir_encounter_id
            fhir_bundle_entry.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_encounter_id is None else fhir_encounter_id if isinstance(fhir_encounter_id, str) else fhir_encounter_id.value)))
            fhir_composition_encounter_reference = malac.models.fhir.r4.Reference()
            fhir_composition.encounter = fhir_composition_encounter_reference
            fhir_composition_encounter_reference.reference = string(value=('urn:uuid:' + ('' if fhir_encounter_id is None else fhir_encounter_id if isinstance(fhir_encounter_id, str) else fhir_encounter_id.value)))
            fhir_composition_encounter_reference.type_ = uri(value='Encounter')
            fhir_diagnosticReport_encounter_reference = malac.models.fhir.r4.Reference()
            fhir_diagnosticReport.encounter = fhir_diagnosticReport_encounter_reference
            fhir_diagnosticReport_encounter_reference.reference = string(value=('urn:uuid:' + ('' if fhir_encounter_id is None else fhir_encounter_id if isinstance(fhir_encounter_id, str) else fhir_encounter_id.value)))
            fhir_diagnosticReport_encounter_reference.type_ = uri(value='Encounter')
            CdaEncompassingEncounterToFhirEncounter(cda_encompassingEncounter, fhir_encounter, fhir_bundle)

def CdaHeaderToFhirDiagnosticReport(cda, fhir_diagnosticReport):
    fhir_diagnosticReport_meta = malac.models.fhir.r4.Meta()
    if fhir_diagnosticReport.meta is not None:
        fhir_diagnosticReport_meta = fhir_diagnosticReport.meta
    else:
        fhir_diagnosticReport.meta = fhir_diagnosticReport_meta
    fhir_diagnosticReport_meta.profile.append(string(value='http://hl7.eu/fhir/laboratory/StructureDefinition/DiagnosticReport-eu-lab'))
    cda_code = cda.code
    if cda_code:
        code_code = cda_code.code
        if code_code:
            fhir_diagnosticReport_category = malac.models.fhir.r4.CodeableConcept()
            fhir_diagnosticReport.category.append(fhir_diagnosticReport_category)
            fhir_diagnosticReport_category.coding.append(translate_single('cda-code-2-fhir-category', (code_code if isinstance(code_code, str) else code_code.value), 'Coding'))
    cda_code = cda.code
    if cda_code:
        for translation in cda_code.translation or []:
            fhir_diagnosticReport.code = malac.models.fhir.r4.CodeableConcept()
            CDCodeableConcept(translation, fhir_diagnosticReport.code)
        if fhirpath.single(fhirpath_utils.bool_not([bool([v2 for v1 in [cda_code] for v2 in fhirpath_utils.get(v1,'translation')])])):
            code_coding = malac.models.fhir.r4.CodeableConcept()
            fhir_diagnosticReport.code = code_coding
            coding_coding = malac.models.fhir.r4.Coding()
            code_coding.coding.append(coding_coding)
            coding_coding.system = uri(value='http://loinc.org')
            coding_coding.code = string(value='11502-2')
    cda_statusCode = cda.statusCode
    if cda_statusCode:
        if fhirpath.single([bool([v2 for v1 in [cda] for v2 in fhirpath_utils.get(v1,'sdtcStatusCode')])]):
            cda_code = cda_statusCode.code
            if cda_code:
                fhir_diagnosticReport.status = string(value=translate_single('cda-sdtc-statuscode-2-fhir-composition-status', (cda_code if isinstance(cda_code, str) else cda_code.value), 'code'))
    if fhirpath.single(fhirpath_utils.bool_not([bool([v2 for v1 in [cda] for v2 in fhirpath_utils.get(v1,'sdtcStatusCode')])])):
        fhir_diagnosticReport.status = string(value='final')
    cda_effectiveTime = cda.effectiveTime
    if cda_effectiveTime:
        fhir_diagnosticReport_effective = malac.models.fhir.r4.dateTime()
        fhir_diagnosticReport.effectiveDateTime = fhir_diagnosticReport_effective
        TSDateTime(cda_effectiveTime, fhir_diagnosticReport_effective)
    if cda.setId:
        fhir_diagnosticReport.identifier.append(malac.models.fhir.r4.Identifier())
        II(cda.setId, fhir_diagnosticReport.identifier[-1])

def CdaPatientRoleToFhirPatient(cda_patientRole, fhir_patient, fhir_bundle):
    fhir_patient_meta = malac.models.fhir.r4.Meta()
    if fhir_patient.meta is not None:
        fhir_patient_meta = fhir_patient.meta
    else:
        fhir_patient.meta = fhir_patient_meta
    fhir_patient_meta.profile.append(string(value='http://hl7.eu/fhir/laboratory/StructureDefinition/Patient-eu-lab'))
    if len(cda_patientRole.id) > 0:
        cda_patientRole_id = cda_patientRole.id[0]
        fhir_patient_identifier = malac.models.fhir.r4.Identifier()
        fhir_patient.identifier.append(fhir_patient_identifier)
        II(cda_patientRole_id, fhir_patient_identifier)
        identifier_type = malac.models.fhir.r4.CodeableConcept()
        if fhir_patient_identifier.type_ is not None:
            identifier_type = fhir_patient_identifier.type_
        else:
            fhir_patient_identifier.type_ = identifier_type
        type_coding = malac.models.fhir.r4.Coding()
        identifier_type.coding.append(type_coding)
        type_coding.system = uri(value='http://terminology.hl7.org/CodeSystem/v2-0203')
        type_coding.code = string(value='PI')
        type_coding.display = string(value='Patient internal identifier')
    for cda_patientRole_id in cda_patientRole.id[1:]:
        fhir_patient_identifier = malac.models.fhir.r4.Identifier()
        fhir_patient.identifier.append(fhir_patient_identifier)
        II(cda_patientRole_id, fhir_patient_identifier)
        if fhirpath.single(fhirpath_utils.equals([v2 for v1 in [cda_patientRole_id] for v2 in fhirpath_utils.get(v1,'root')], '==', ['1.2.40.0.10.1.4.3.1'])):
            assigner = malac.models.fhir.r4.Reference()
            if fhir_patient_identifier.assigner is not None:
                assigner = fhir_patient_identifier.assigner
            else:
                fhir_patient_identifier.assigner = assigner
            assigner.display = string(value='Dachverband der Ã¶sterreichischen SozialversicherungstrÃ¤ger')
            identifier_type = malac.models.fhir.r4.CodeableConcept()
            if fhir_patient_identifier.type_ is not None:
                identifier_type = fhir_patient_identifier.type_
            else:
                fhir_patient_identifier.type_ = identifier_type
            type_coding = malac.models.fhir.r4.Coding()
            identifier_type.coding.append(type_coding)
            type_coding.system = uri(value='http://terminology.hl7.org/CodeSystem/v2-0203')
            type_coding.code = string(value='SS')
            type_coding.display = string(value='Social Security Number')
        if fhirpath.single(fhirpath_utils.equals([v2 for v1 in [cda_patientRole_id] for v2 in fhirpath_utils.get(v1,'root')], '==', ['1.2.40.0.10.2.1.1.149'])):
            assigner = malac.models.fhir.r4.Reference()
            if fhir_patient_identifier.assigner is not None:
                assigner = fhir_patient_identifier.assigner
            else:
                fhir_patient_identifier.assigner = assigner
            assigner.display = string(value='Bundesministerium fÃ¼r Inneres')
            identifier_type = malac.models.fhir.r4.CodeableConcept()
            if fhir_patient_identifier.type_ is not None:
                identifier_type = fhir_patient_identifier.type_
            else:
                fhir_patient_identifier.type_ = identifier_type
            type_coding = malac.models.fhir.r4.Coding()
            identifier_type.coding.append(type_coding)
            type_coding.system = uri(value='http://terminology.hl7.org/CodeSystem/v2-0203')
            type_coding.code = string(value='NI')
            type_coding.display = string(value='National unique individual identifier')
    for addr in cda_patientRole.addr or []:
        fhir_patient.address.append(malac.models.fhir.r4.Address())
        CdaAdressCompilationToFhirAustrianAddress(addr, fhir_patient.address[-1])
    for telecom in cda_patientRole.telecom or []:
        fhir_patient.telecom.append(malac.models.fhir.r4.ContactPoint())
        TELContactPoint(telecom, fhir_patient.telecom[-1])
    cda_patient = cda_patientRole.patient
    if cda_patient:
        for name in cda_patient.name or []:
            fhir_patient.name.append(malac.models.fhir.r4.HumanName())
            CdaPersonNameCompilationToFhirHumanName(name, fhir_patient.name[-1])
        cda_patient_gender = cda_patient.administrativeGenderCode
        if cda_patient_gender:
            cda_patient_gender_code = cda_patient_gender.code
            if cda_patient_gender_code:
                fhir_patient.gender = string(value=translate_single('ELGAAdministrativeGenderFHIRGender', (cda_patient_gender_code if isinstance(cda_patient_gender_code, str) else cda_patient_gender_code.value), 'code'))
        if cda_patient.birthTime:
            fhir_patient.birthDate = malac.models.fhir.r4.date()
            TSDate(cda_patient.birthTime, fhir_patient.birthDate)
        cda_patient_birthTime = cda_patient.birthTime
        if cda_patient_birthTime:
            if fhirpath.single(fhirpath_utils.compare([v6 for v5 in fhirpath_utils.toString([v4 for v3 in [v2 for v1 in [cda_patient] for v2 in fhirpath_utils.get(v1,'birthTime')] for v4 in fhirpath_utils.get(v3,'value')]) for v6 in fhirpath_utils.strlength(v5)], '>', [10])):
                fhir_patient_birthDate = malac.models.fhir.r4.date()
                if fhir_patient.birthDate is not None:
                    fhir_patient_birthDate = fhir_patient.birthDate
                else:
                    fhir_patient.birthDate = fhir_patient_birthDate
                extension = malac.models.fhir.r4.Extension()
                fhir_patient_birthDate.extension.append(extension)
                extension.url = 'http://hl7.org/fhir/StructureDefinition/patient-birthTime'
                fhir_patient_birthTime_dateTime = malac.models.fhir.r4.dateTime()
                extension.valueDateTime = fhir_patient_birthTime_dateTime
                TSDateTime(cda_patient_birthTime, fhir_patient_birthTime_dateTime)
        cda_patient_deceasedInd = cda_patient.deceasedInd
        if cda_patient_deceasedInd:
            if fhirpath.single([not([v2 for v1 in [cda_patient] for v2 in fhirpath_utils.get(v1,'sdtcDeceasedTime')])]):
                fhir_patient_deceased = malac.models.fhir.r4.boolean()
                fhir_patient.deceasedBoolean = fhir_patient_deceased
                BL(cda_patient_deceasedInd, fhir_patient_deceased)
        cda_patient_deceasedTime = cda_patient.deceasedTime
        if cda_patient_deceasedTime:
            fhir_patient_deceased = malac.models.fhir.r4.dateTime()
            fhir_patient.deceasedDateTime = fhir_patient_deceased
            TSDateTime(cda_patient_deceasedTime, fhir_patient_deceased)
        if cda_patient.maritalStatusCode:
            fhir_patient.maritalStatus = malac.models.fhir.r4.CodeableConcept()
            transform_default(cda_patient.maritalStatusCode, fhir_patient.maritalStatus)
        cda_patient_religiousAffiliationCode = cda_patient.religiousAffiliationCode
        if cda_patient_religiousAffiliationCode:
            religion_extension = malac.models.fhir.r4.Extension()
            fhir_patient.extension.append(religion_extension)
            religion_extension.url = 'http://hl7.org/fhir/StructureDefinition/patient-religion'
            religion_extension_codeableConcept = malac.models.fhir.r4.CodeableConcept()
            religion_extension.valueCodeableConcept = religion_extension_codeableConcept
            CECodeableConcept(cda_patient_religiousAffiliationCode, religion_extension_codeableConcept)
        for cda_patient_guardian in cda_patient.guardian or []:
            fhir_patient_contact = malac.models.fhir.r4.Patient_Contact()
            fhir_patient.contact.append(fhir_patient_contact)
            for addr_ in cda_patient_guardian.addr or []:
                fhir_patient_contact.address = malac.models.fhir.r4.Address()
                CdaAdressCompilationToFhirAustrianAddress(addr_, fhir_patient_contact.address)
            for telecom_ in cda_patient_guardian.telecom or []:
                fhir_patient_contact.telecom.append(malac.models.fhir.r4.ContactPoint())
                TELContactPoint(telecom_, fhir_patient_contact.telecom[-1])
            cda_guardian_person = cda_patient_guardian.guardianPerson
            if cda_guardian_person:
                for name_ in cda_guardian_person.name or []:
                    fhir_patient_contact.name = malac.models.fhir.r4.HumanName()
                    CdaPersonNameCompilationToFhirHumanName(name_, fhir_patient_contact.name)
            cda_guardian_organization = cda_patient_guardian.guardianOrganization
            if cda_guardian_organization:
                for cda_organization_name in cda_guardian_organization.name or []:
                    fhir_bundle_entry = malac.models.fhir.r4.Bundle_Entry()
                    fhir_bundle.entry.append(fhir_bundle_entry)
                    fhir_contact_organization = malac.models.fhir.r4.Organization()
                    fhir_bundle_entry.resource = malac.models.fhir.r4.ResourceContainer(Organization=fhir_contact_organization)
                    fhir_contact_organization_id = string(value=str(uuid.uuid4()))
                    fhir_contact_organization.id = fhir_contact_organization_id
                    fhir_contact_organization.name = string(value=fhirpath.single([v2 for v1 in [cda_organization_name] for v2 in fhirpath_utils.get(v1,'valueOf_',strip=True)]))
                    fhir_bundle_entry.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_contact_organization_id is None else fhir_contact_organization_id if isinstance(fhir_contact_organization_id, str) else fhir_contact_organization_id.value)))
                    fhir_contact_organization_reference = malac.models.fhir.r4.Reference()
                    fhir_patient_contact.organization = fhir_contact_organization_reference
                    fhir_contact_organization_reference.reference = string(value=('urn:uuid:' + ('' if fhir_contact_organization_id is None else fhir_contact_organization_id if isinstance(fhir_contact_organization_id, str) else fhir_contact_organization_id.value)))
        cda_patient_birthplace = cda_patient.birthplace
        if cda_patient_birthplace:
            cda_patient_place = cda_patient_birthplace.place
            if cda_patient_place:
                cda_patient_birthaddr = cda_patient_place.addr
                if cda_patient_birthaddr:
                    birthplace_extension = malac.models.fhir.r4.Extension()
                    fhir_patient.extension.append(birthplace_extension)
                    birthplace_extension.url = 'http://hl7.org/fhir/StructureDefinition/patient-birthPlace'
                    birthplace_extension_addr = malac.models.fhir.r4.Address()
                    birthplace_extension.valueAddress = birthplace_extension_addr
                    CdaAdressCompilationToFhirAustrianAddress(cda_patient_birthaddr, birthplace_extension_addr)
        for cda_patient_language in cda_patient.languageCommunication or []:
            fhir_patient_communication = malac.models.fhir.r4.Patient_Communication()
            fhir_patient.communication.append(fhir_patient_communication)
            cda_patient_languageCode = cda_patient_language.languageCode
            if cda_patient_languageCode:
                cda_patient_languageCode_code = cda_patient_languageCode.code
                if cda_patient_languageCode_code:
                    fhir_patient_communication_language = malac.models.fhir.r4.CodeableConcept()
                    if fhir_patient_communication.language is not None:
                        fhir_patient_communication_language = fhir_patient_communication.language
                    else:
                        fhir_patient_communication.language = fhir_patient_communication_language
                    fhir_patient_communication_language_coding = malac.models.fhir.r4.Coding()
                    fhir_patient_communication_language.coding.append(fhir_patient_communication_language_coding)
                    fhir_patient_communication_language_coding.system = uri(value='urn:ietf:bcp:47')
                    fhir_patient_communication_language_coding.code = string(value=cda_patient_languageCode_code)
            if cda_patient_language.preferenceInd:
                fhir_patient_communication.preferred = malac.models.fhir.r4.boolean()
                BL(cda_patient_language.preferenceInd, fhir_patient_communication.preferred)
            if fhirpath.single(fhirpath_utils.bool_or([bool([v2 for v1 in [cda_patient_language] for v2 in fhirpath_utils.get(v1,'modeCode')])], [bool([v5 for v4 in [cda_patient_language] for v5 in fhirpath_utils.get(v4,'proficiencyLevelCode')])])):
                communication_extension = malac.models.fhir.r4.Extension()
                fhir_patient_communication.extension.append(communication_extension)
                communication_extension.url = 'http://hl7.org/fhir/StructureDefinition/patient-proficiency'
                cda_patient_language_modeCode = cda_patient_language.modeCode
                if cda_patient_language_modeCode:
                    communication_extension_type = malac.models.fhir.r4.Extension()
                    communication_extension.extension.append(communication_extension_type)
                    communication_extension_type.url = 'type'
                    communication_extension_type_coding = malac.models.fhir.r4.Coding()
                    communication_extension_type.valueCoding = communication_extension_type_coding
                    CECoding(cda_patient_language_modeCode, communication_extension_type_coding)
                cda_patient_language_proficiencyLevelCode = cda_patient_language.proficiencyLevelCode
                if cda_patient_language_proficiencyLevelCode:
                    communication_extension_level = malac.models.fhir.r4.Extension()
                    communication_extension.extension.append(communication_extension_level)
                    communication_extension_level.url = 'level'
                    communication_extension_level_coding = malac.models.fhir.r4.Coding()
                    communication_extension_level.valueCoding = communication_extension_level_coding
                    CECoding(cda_patient_language_proficiencyLevelCode, communication_extension_level_coding)

def CdaAuthorToFhirPractitionerRole(cda_author, fhir_practitionerRole, fhir_bundle):
    fhir_bundle_entry = malac.models.fhir.r4.Bundle_Entry()
    fhir_bundle.entry.append(fhir_bundle_entry)
    fhir_practitioner = malac.models.fhir.r4.Practitioner()
    fhir_bundle_entry.resource = malac.models.fhir.r4.ResourceContainer(Practitioner=fhir_practitioner)
    fhir_practitioner_id = string(value=str(uuid.uuid4()))
    fhir_practitioner.id = fhir_practitioner_id
    fhir_bundle_entry.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_practitioner_id is None else fhir_practitioner_id if isinstance(fhir_practitioner_id, str) else fhir_practitioner_id.value)))
    fhir_practitionerRole_practitioner_reference = malac.models.fhir.r4.Reference()
    fhir_practitionerRole.practitioner = fhir_practitionerRole_practitioner_reference
    fhir_practitionerRole_practitioner_reference.reference = string(value=('urn:uuid:' + ('' if fhir_practitioner_id is None else fhir_practitioner_id if isinstance(fhir_practitioner_id, str) else fhir_practitioner_id.value)))
    fhir_practitionerRole_practitioner_reference.type_ = uri(value='Practitioner')
    if cda_author.functionCode:
        fhir_practitionerRole.code.append(malac.models.fhir.r4.CodeableConcept())
        transform_default(cda_author.functionCode, fhir_practitionerRole.code[-1])
    cda_author_assignedAuthor = cda_author.assignedAuthor
    if cda_author_assignedAuthor:
        for id_ in cda_author_assignedAuthor.id or []:
            fhir_practitioner.identifier.append(malac.models.fhir.r4.Identifier())
            II(id_, fhir_practitioner.identifier[-1])
        cda_author_assignedAuthor_code = cda_author_assignedAuthor.code
        if cda_author_assignedAuthor_code:
            fhir_practitioner_qualification = malac.models.fhir.r4.Practitioner_Qualification()
            fhir_practitioner.qualification.append(fhir_practitioner_qualification)
            fhir_practitioner_qualification_code = malac.models.fhir.r4.CodeableConcept()
            if fhir_practitioner_qualification.code is not None:
                fhir_practitioner_qualification_code = fhir_practitioner_qualification.code
            else:
                fhir_practitioner_qualification.code = fhir_practitioner_qualification_code
            CECodeableConcept(cda_author_assignedAuthor_code, fhir_practitioner_qualification_code)
        for telecom in cda_author_assignedAuthor.telecom or []:
            fhir_practitioner.telecom.append(malac.models.fhir.r4.ContactPoint())
            TELContactPoint(telecom, fhir_practitioner.telecom[-1])
        cda_assignedPerson = cda_author_assignedAuthor.assignedPerson
        if cda_assignedPerson:
            for name in cda_assignedPerson.name or []:
                fhir_practitioner.name.append(malac.models.fhir.r4.HumanName())
                CdaPersonNameCompilationToFhirHumanName(name, fhir_practitioner.name[-1])
        cda_representedOrganization = cda_author_assignedAuthor.representedOrganization
        if cda_representedOrganization:
            fhir_bundle_entry = malac.models.fhir.r4.Bundle_Entry()
            fhir_bundle.entry.append(fhir_bundle_entry)
            fhir_organization = malac.models.fhir.r4.Organization()
            fhir_bundle_entry.resource = malac.models.fhir.r4.ResourceContainer(Organization=fhir_organization)
            fhir_organization_id = string(value=str(uuid.uuid4()))
            fhir_organization.id = fhir_organization_id
            fhir_bundle_entry.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_organization_id is None else fhir_organization_id if isinstance(fhir_organization_id, str) else fhir_organization_id.value)))
            fhir_practitionerRole_organization = malac.models.fhir.r4.Reference()
            fhir_practitionerRole.organization = fhir_practitionerRole_organization
            fhir_practitionerRole_organization.reference = string(value=('urn:uuid:' + ('' if fhir_organization_id is None else fhir_organization_id if isinstance(fhir_organization_id, str) else fhir_organization_id.value)))
            fhir_practitionerRole_organization.type_ = uri(value='Organization')
            CdaOrganizationCompilationToFhirOrganization(cda_representedOrganization, fhir_organization)

def CdaAuthorToFhirDevice(cda_author, fhir_device, fhir_bundle):
    if cda_author.functionCode:
        fhir_device.type_ = malac.models.fhir.r4.CodeableConcept()
        transform_default(cda_author.functionCode, fhir_device.type_)
    cda_author_assignedAuthor = cda_author.assignedAuthor
    if cda_author_assignedAuthor:
        for id_ in cda_author_assignedAuthor.id or []:
            fhir_device.identifier.append(malac.models.fhir.r4.Identifier())
            II(id_, fhir_device.identifier[-1])
        for telecom in cda_author_assignedAuthor.telecom or []:
            fhir_device.contact.append(malac.models.fhir.r4.ContactPoint())
            TELContactPoint(telecom, fhir_device.contact[-1])
        cda_assignedAuthoringDevice = cda_author_assignedAuthor.assignedAuthoringDevice
        if cda_assignedAuthoringDevice:
            cda_manufacturerModelName = cda_assignedAuthoringDevice.manufacturerModelName
            if cda_manufacturerModelName:
                fhir_device_deviceName = malac.models.fhir.r4.Device_DeviceName()
                fhir_device.deviceName.append(fhir_device_deviceName)
                fhir_device_deviceName.name = string(value=fhirpath.single([v2 for v1 in [cda_manufacturerModelName] for v2 in fhirpath_utils.get(v1,'valueOf_',strip=True)]))
                fhir_device_deviceName.type_ = string(value='model-name')
            cda_softwareName = cda_assignedAuthoringDevice.softwareName
            if cda_softwareName:
                fhir_device_deviceName = malac.models.fhir.r4.Device_DeviceName()
                fhir_device.deviceName.append(fhir_device_deviceName)
                fhir_device_deviceName.name = string(value=fhirpath.single([v2 for v1 in [cda_softwareName] for v2 in fhirpath_utils.get(v1,'valueOf_',strip=True)]))
                fhir_device_deviceName.type_ = string(value='other')
        cda_representedOrganization = cda_author_assignedAuthor.representedOrganization
        if cda_representedOrganization:
            fhir_bundle_entry = malac.models.fhir.r4.Bundle_Entry()
            fhir_bundle.entry.append(fhir_bundle_entry)
            fhir_organization = malac.models.fhir.r4.Organization()
            fhir_bundle_entry.resource = malac.models.fhir.r4.ResourceContainer(Organization=fhir_organization)
            fhir_organization_id = string(value=str(uuid.uuid4()))
            fhir_organization.id = fhir_organization_id
            fhir_bundle_entry.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_organization_id is None else fhir_organization_id if isinstance(fhir_organization_id, str) else fhir_organization_id.value)))
            fhir_device_owner = malac.models.fhir.r4.Reference()
            fhir_device.owner = fhir_device_owner
            fhir_device_owner.reference = string(value=('urn:uuid:' + ('' if fhir_organization_id is None else fhir_organization_id if isinstance(fhir_organization_id, str) else fhir_organization_id.value)))
            fhir_device_owner.type_ = uri(value='Organization')
            CdaOrganizationCompilationToFhirOrganization(cda_representedOrganization, fhir_organization)

def CdaEncompassingEncounterToFhirEncounter(cda_encompassingEncounter, fhir_encounter, fhir_bundle):
    for id_ in cda_encompassingEncounter.id or []:
        fhir_encounter.identifier.append(malac.models.fhir.r4.Identifier())
        II(id_, fhir_encounter.identifier[-1])
    fhir_encounter.status = string(value='finished')
    if cda_encompassingEncounter.code:
        fhir_encounter.class_ = malac.models.fhir.r4.Coding()
        transform_default(cda_encompassingEncounter.code, fhir_encounter.class_)
    if cda_encompassingEncounter.effectiveTime:
        fhir_encounter.period = malac.models.fhir.r4.Period()
        IVLTSPeriod(cda_encompassingEncounter.effectiveTime, fhir_encounter.period)
    cda_responsibleParty = cda_encompassingEncounter.responsibleParty
    if cda_responsibleParty:
        cda_assignedEntity = cda_responsibleParty.assignedEntity
        if cda_assignedEntity:
            fhir_encounter_participant = malac.models.fhir.r4.Encounter_Participant()
            fhir_encounter.participant.append(fhir_encounter_participant)
            fhir_bundle_entry = malac.models.fhir.r4.Bundle_Entry()
            fhir_bundle.entry.append(fhir_bundle_entry)
            fhir_practitionerRole = malac.models.fhir.r4.PractitionerRole()
            fhir_bundle_entry.resource = malac.models.fhir.r4.ResourceContainer(PractitionerRole=fhir_practitionerRole)
            fhir_practitionerRole_id = string(value=str(uuid.uuid4()))
            fhir_practitionerRole.id = fhir_practitionerRole_id
            fhir_bundle_entry.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_practitionerRole_id is None else fhir_practitionerRole_id if isinstance(fhir_practitionerRole_id, str) else fhir_practitionerRole_id.value)))
            fhir_practitionerRole_reference = malac.models.fhir.r4.Reference()
            fhir_encounter_participant.individual = fhir_practitionerRole_reference
            fhir_practitionerRole_reference.reference = string(value=('urn:uuid:' + ('' if fhir_practitionerRole_id is None else fhir_practitionerRole_id if isinstance(fhir_practitionerRole_id, str) else fhir_practitionerRole_id.value)))
            fhir_practitionerRole_reference.type_ = uri(value='PractitionerRole')
            CdaAssignedEntityToFhirPractitionerRole(cda_assignedEntity, fhir_practitionerRole, fhir_bundle)
    cda_location = cda_encompassingEncounter.location
    if cda_location:
        cda_healthCareFacility = cda_location.healthCareFacility
        if cda_healthCareFacility:
            fhir_encounter_location = malac.models.fhir.r4.Encounter_Location()
            fhir_encounter.location.append(fhir_encounter_location)
            fhir_bundle_entry = malac.models.fhir.r4.Bundle_Entry()
            fhir_bundle.entry.append(fhir_bundle_entry)
            fhir_location = malac.models.fhir.r4.Location()
            fhir_bundle_entry.resource = malac.models.fhir.r4.ResourceContainer(Location=fhir_location)
            fhir_location_id = string(value=str(uuid.uuid4()))
            fhir_location.id = fhir_location_id
            fhir_bundle_entry.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_location_id is None else fhir_location_id if isinstance(fhir_location_id, str) else fhir_location_id.value)))
            fhir_location_reference = malac.models.fhir.r4.Reference()
            fhir_encounter_location.location = fhir_location_reference
            fhir_location_reference.reference = string(value=('urn:uuid:' + ('' if fhir_location_id is None else fhir_location_id if isinstance(fhir_location_id, str) else fhir_location_id.value)))
            fhir_location_reference.type_ = uri(value='Location')
            if cda_healthCareFacility.code:
                fhir_location.type_.append(malac.models.fhir.r4.CodeableConcept())
                transform_default(cda_healthCareFacility.code, fhir_location.type_[-1])
            cda_serviceProviderOrganization = cda_healthCareFacility.serviceProviderOrganization
            if cda_serviceProviderOrganization:
                fhir_bundle_entry = malac.models.fhir.r4.Bundle_Entry()
                fhir_bundle.entry.append(fhir_bundle_entry)
                fhir_organization = malac.models.fhir.r4.Organization()
                fhir_bundle_entry.resource = malac.models.fhir.r4.ResourceContainer(Organization=fhir_organization)
                fhir_organization_id = string(value=str(uuid.uuid4()))
                fhir_organization.id = fhir_organization_id
                fhir_bundle_entry.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_organization_id is None else fhir_organization_id if isinstance(fhir_organization_id, str) else fhir_organization_id.value)))
                fhir_location_managingOrganization = malac.models.fhir.r4.Reference()
                fhir_location.managingOrganization = fhir_location_managingOrganization
                fhir_location_managingOrganization.reference = string(value=('urn:uuid:' + ('' if fhir_organization_id is None else fhir_organization_id if isinstance(fhir_organization_id, str) else fhir_organization_id.value)))
                fhir_location_managingOrganization.type_ = uri(value='Organization')
                CdaOrganizationCompilationToFhirOrganization(cda_serviceProviderOrganization, fhir_organization)

def CdaBodyToFhirComposition(cda, cda_structuredBody, fhir_composition, fhir_practitionerRole, fhir_patient, fhir_diagnosticReport, fhir_bundle):
    for cda_component in cda_structuredBody.component or []:
        cda_section = cda_component.section
        if cda_section:
            if fhirpath.single(fhirpath_utils.bool_or(fhirpath_utils.bool_or(fhirpath_utils.bool_or(fhirpath_utils.bool_or([v1 for v1 in fhirpath_utils.get(cda_section,'code') if fhirpath_utils.bool_and(fhirpath_utils.equals(fhirpath_utils.get(v1,'code'), '==', ['BRIEFT']), fhirpath_utils.equals(fhirpath_utils.get(v1,'codeSystem'), '==', ['1.2.40.0.34.5.40'])) == [True]], (fhirpath_utils.bool_and([v2 for v2 in fhirpath_utils.get(cda_section,'code') if fhirpath_utils.bool_and(fhirpath_utils.equals(fhirpath_utils.get(v2,'code'), '==', ['46239-0']), fhirpath_utils.equals(fhirpath_utils.get(v2,'codeSystem'), '==', ['2.16.840.1.113883.6.1'])) == [True]], (fhirpath_utils.bool_or([v3 for v3 in fhirpath_utils.get(cda_section,'templateId') if fhirpath_utils.equals(fhirpath_utils.get(v3,'root'), '==', ['1.2.40.0.34.6.0.11.2.114']) == [True]], [v4 for v4 in fhirpath_utils.get(cda_section,'templateId') if fhirpath_utils.equals(fhirpath_utils.get(v4,'root'), '==', ['1.2.40.0.34.11.4.2.4']) == [True]]))))), (fhirpath_utils.bool_and([v5 for v5 in fhirpath_utils.get(cda_section,'code') if fhirpath_utils.bool_and(fhirpath_utils.equals(fhirpath_utils.get(v5,'code'), '==', ['10164-2']), fhirpath_utils.equals(fhirpath_utils.get(v5,'codeSystem'), '==', ['2.16.840.1.113883.6.1'])) == [True]], [v6 for v6 in fhirpath_utils.get(cda_section,'templateId') if fhirpath_utils.equals(fhirpath_utils.get(v6,'root'), '==', ['1.2.40.0.34.6.0.11.2.111']) == [True]]))), (fhirpath_utils.bool_and([v7 for v7 in fhirpath_utils.get(cda_section,'code') if fhirpath_utils.bool_and(fhirpath_utils.equals(fhirpath_utils.get(v7,'code'), '==', ['400999005']), fhirpath_utils.equals(fhirpath_utils.get(v7,'codeSystem'), '==', ['2.16.840.1.113883.6.96'])) == [True]], [v8 for v8 in fhirpath_utils.get(cda_section,'templateId') if fhirpath_utils.equals(fhirpath_utils.get(v8,'root'), '==', ['1.2.40.0.34.6.0.11.2.112']) == [True]]))), (fhirpath_utils.bool_and([v9 for v9 in fhirpath_utils.get(cda_section,'code') if fhirpath_utils.bool_and(fhirpath_utils.equals(fhirpath_utils.get(v9,'code'), '==', ['ABBEM']), fhirpath_utils.equals(fhirpath_utils.get(v9,'codeSystem'), '==', ['1.2.40.0.34.5.40'])) == [True]], [v10 for v10 in fhirpath_utils.get(cda_section,'templateId') if fhirpath_utils.equals(fhirpath_utils.get(v10,'root'), '==', ['1.2.40.0.34.6.0.11.2.70']) == [True]])))):
                fhir_section = malac.models.fhir.r4.Composition_Section()
                fhir_composition.section.append(fhir_section)
                CdaSectionToFhirSection(cda_section, fhir_section, fhir_bundle)
        cda_section = cda_component.section
        if cda_section:
            if fhirpath.single([v1 for v1 in fhirpath_utils.get(cda_section,'code') if fhirpath_utils.bool_and(fhirpath_utils.equals(fhirpath_utils.get(v1,'code'), '==', ['10']), fhirpath_utils.equals(fhirpath_utils.get(v1,'codeSystem'), '==', ['1.2.40.0.34.5.11'])) == [True]]):
                CdaSpecimenSectionToFhirSpecimen(cda_section, fhir_patient, fhir_diagnosticReport, fhir_bundle)
        cda_section = cda_component.section
        if cda_section:
            if fhirpath.single([v1 for v1 in fhirpath_utils.get(cda_section,'templateId') if fhirpath_utils.bool_or(fhirpath_utils.equals(fhirpath_utils.get(v1,'root'), '==', ['1.2.40.0.34.6.0.11.2.102']), fhirpath_utils.equals(fhirpath_utils.get(v1,'root'), '==', ['1.3.6.1.4.1.19376.1.3.3.2.1'])) == [True]]):
                fhir_section = malac.models.fhir.r4.Composition_Section()
                fhir_composition.section.append(fhir_section)
                CdaLaboratorySpecialtySectionToFhirSection(cda, cda_section, fhir_section, fhir_practitionerRole, fhir_patient, fhir_diagnosticReport, fhir_bundle)
        cda_section = cda_component.section
        if cda_section:
            if fhirpath.single([v1 for v1 in fhirpath_utils.get(cda_section,'code') if fhirpath_utils.bool_and(fhirpath_utils.equals(fhirpath_utils.get(v1,'code'), '==', ['20']), fhirpath_utils.equals(fhirpath_utils.get(v1,'codeSystem'), '==', ['1.2.40.0.34.5.11'])) == [True]]):
                fhir_section = malac.models.fhir.r4.Composition_Section()
                fhir_composition.section.append(fhir_section)
                CdaBefundbewertungSectionToFhirSection(cda_section, fhir_section, fhir_bundle)
        cda_section = cda_component.section
        if cda_section:
            if fhirpath.single([v1 for v1 in fhirpath_utils.get(cda_section,'code') if fhirpath_utils.bool_and(fhirpath_utils.equals(fhirpath_utils.get(v1,'code'), '==', ['BEIL']), fhirpath_utils.equals(fhirpath_utils.get(v1,'codeSystem'), '==', ['1.2.40.0.34.5.40'])) == [True]]):
                CdaBeilagenSectionToFhirDiagnosticReportMedia(cda_section, fhir_diagnosticReport, fhir_bundle, fhir_patient)
        cda_section = cda_component.section
        if cda_section:
            if fhirpath.single(fhirpath_utils.bool_and([v1 for v1 in fhirpath_utils.get(cda_section,'code') if fhirpath_utils.bool_and(fhirpath_utils.equals(fhirpath_utils.get(v1,'code'), '==', ['408773008']), fhirpath_utils.equals(fhirpath_utils.get(v1,'codeSystem'), '==', ['2.16.840.1.113883.6.96'])) == [True]], [v2 for v2 in fhirpath_utils.get(cda_section,'templateId') if fhirpath_utils.equals(fhirpath_utils.get(v2,'root'), '==', ['1.2.40.0.34.6.0.11.2.79']) == [True]])):
                fhir_section = malac.models.fhir.r4.Composition_Section()
                fhir_composition.section.append(fhir_section)
                CdaSectionToFhirSection(cda_section, fhir_section, fhir_bundle)
        cda_section = cda_component.section
        if cda_section:
            if fhirpath.single(fhirpath_utils.bool_and([v1 for v1 in fhirpath_utils.get(cda_section,'code') if fhirpath_utils.bool_and(fhirpath_utils.equals(fhirpath_utils.get(v1,'code'), '==', ['721917003']), fhirpath_utils.equals(fhirpath_utils.get(v1,'codeSystem'), '==', ['2.16.840.1.113883.6.96'])) == [True]], [v2 for v2 in fhirpath_utils.get(cda_section,'templateId') if fhirpath_utils.equals(fhirpath_utils.get(v2,'root'), '==', ['1.2.40.0.34.6.0.11.2.80']) == [True]])):
                fhir_section = malac.models.fhir.r4.Composition_Section()
                fhir_composition.section.append(fhir_section)
                CdaZusammenfassungBehandlungSectionToFhir(cda_section, fhir_section, fhir_bundle)
        cda_section = cda_component.section
        if cda_section:
            if fhirpath.single([v1 for v1 in fhirpath_utils.get(cda_section,'code') if fhirpath_utils.bool_and(fhirpath_utils.equals(fhirpath_utils.get(v1,'code'), '==', ['703852005']), fhirpath_utils.equals(fhirpath_utils.get(v1,'codeSystem'), '==', ['2.16.840.1.113883.6.96'])) == [True]]):
                fhir_section = malac.models.fhir.r4.Composition_Section()
                fhir_composition.section.append(fhir_section)
                CdaAuszugErhobeneDatenSectionToFhir(cda_section, fhir_section, fhir_bundle)
        cda_section = cda_component.section
        if cda_section:
            if fhirpath.single([v1 for v1 in fhirpath_utils.get(cda_section,'templateId') if fhirpath_utils.equals(fhirpath_utils.get(v1,'root'), '==', ['1.2.40.0.34.6.0.11.2.96']) == [True]]):
                fhir_section = malac.models.fhir.r4.Composition_Section()
                fhir_composition.section.append(fhir_section)
                CdaDiagnosisToFhirSection(cda, cda_section, fhir_section, fhir_practitionerRole, fhir_patient, fhir_diagnosticReport, fhir_bundle)

def CdaToPractitionerRole(cda, fhir_practitionerRole, fhir_bundle):
    if fhirpath.single([bool([v6 for v5 in [v4 for v3 in fhirpath_utils.at_index([v2 for v1 in [cda] for v2 in fhirpath_utils.get(v1,'documentationOf')], [0]) for v4 in fhirpath_utils.get(v3,'serviceEvent')] for v6 in fhirpath_utils.get(v5,'performer')])]):
        if len(cda.documentationOf) > 0:
            cda_documentationOf = cda.documentationOf[0]
            cda_documentationOf_serviceEvent = cda_documentationOf.serviceEvent
            if cda_documentationOf_serviceEvent:
                for cda_documentationOf_serviceEvent_performer in cda_documentationOf_serviceEvent.performer or []:
                    cda_performer_assignedEntity = cda_documentationOf_serviceEvent_performer.assignedEntity
                    if cda_performer_assignedEntity:
                        CdaAssignedEntityToFhirPractitionerRole(cda_performer_assignedEntity, fhir_practitionerRole, fhir_bundle)
    if fhirpath.single(fhirpath_utils.bool_not([bool([v6 for v5 in [v4 for v3 in fhirpath_utils.at_index([v2 for v1 in [cda] for v2 in fhirpath_utils.get(v1,'documentationOf')], [0]) for v4 in fhirpath_utils.get(v3,'serviceEvent')] for v6 in fhirpath_utils.get(v5,'performer')])])):
        for cda_author in cda.author:
            if fhirpath.single([bool([v4 for v3 in [v2 for v1 in [cda_author] for v2 in fhirpath_utils.get(v1,'assignedAuthor')] for v4 in fhirpath_utils.get(v3,'assignedPerson')])]):
                CdaAuthorToFhirPractitionerRole(cda_author, fhir_practitionerRole, fhir_bundle)

def CdaSectionToFhirSection(cda_section, fhir_section, fhir_bundle):
    if cda_section.code:
        fhir_section.code = malac.models.fhir.r4.CodeableConcept()
        transform_default(cda_section.code, fhir_section.code)
    cda_section_title = cda_section.title
    if cda_section_title:
        fhir_section.title = string(value=fhirpath.single([v2 for v1 in [cda_section_title] for v2 in fhirpath_utils.get(v1,'valueOf_',strip=True)]))
    cda_section_text = cda_section.text
    if cda_section_text:
        fhir_section_text = malac.models.fhir.r4.Narrative()
        if fhir_section.text is not None:
            fhir_section_text = fhir_section.text
        else:
            fhir_section.text = fhir_section_text
        fhir_section_text.status = string(value='generated')
        if fhirpath.single(fhirpath_utils.bool_not([bool([v2 for v1 in [cda_section] for v2 in fhirpath_utils.get(v1,'languageCode')])])):
            fhir_section_text.div = utils.strucdoctext2html(malac.models.fhir.r4, cda_section_text)
        if fhirpath.single([bool([v2 for v1 in [cda_section] for v2 in fhirpath_utils.get(v1,'languageCode')])]):
            cda_languageCode = cda_section.languageCode
            if cda_languageCode:
                cda_languageCode_code = cda_languageCode.code
                if cda_languageCode_code:
                    fhir_section_text.div = utils.strucdoctext2html(malac.models.fhir.r4, cda_section_text)
    for cda_section_author in cda_section.author or []:
        fhir_bundle_entry = malac.models.fhir.r4.Bundle_Entry()
        fhir_bundle.entry.append(fhir_bundle_entry)
        fhir_practitionerRole = malac.models.fhir.r4.PractitionerRole()
        fhir_bundle_entry.resource = malac.models.fhir.r4.ResourceContainer(PractitionerRole=fhir_practitionerRole)
        fhir_practitionerRole_id = string(value=str(uuid.uuid4()))
        fhir_practitionerRole.id = fhir_practitionerRole_id
        fhir_bundle_entry.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_practitionerRole_id is None else fhir_practitionerRole_id if isinstance(fhir_practitionerRole_id, str) else fhir_practitionerRole_id.value)))
        fhir_section_author_reference = malac.models.fhir.r4.Reference()
        fhir_section.author.append(fhir_section_author_reference)
        fhir_section_author_reference.reference = string(value=('urn:uuid:' + ('' if fhir_practitionerRole_id is None else fhir_practitionerRole_id if isinstance(fhir_practitionerRole_id, str) else fhir_practitionerRole_id.value)))
        fhir_section_author_reference.type_ = uri(value='PractitionerRole')
        CdaAuthorToFhirPractitionerRole(cda_section_author, fhir_practitionerRole, fhir_bundle)

def CdaSpecimenSectionToFhirSpecimen(cda_section, fhir_patient, fhir_diagnosticReport, fhir_bundle):
    for cda_section_entry in cda_section.entry or []:
        cda_act = cda_section_entry.act
        if cda_act:
            if fhirpath.single([v3 for v3 in [v2 for v1 in [cda_act] for v2 in fhirpath_utils.get(v1,'code')] if fhirpath_utils.equals(fhirpath_utils.get(v3,'code'), '==', ['10']) == [True]]):
                for cda_entryRelationship in cda_act.entryRelationship or []:
                    cda_procedure = cda_entryRelationship.procedure
                    if cda_procedure:
                        fhir_bundle_entry = malac.models.fhir.r4.Bundle_Entry()
                        fhir_bundle.entry.append(fhir_bundle_entry)
                        fhir_specimen = malac.models.fhir.r4.Specimen()
                        fhir_bundle_entry.resource = malac.models.fhir.r4.ResourceContainer(Specimen=fhir_specimen)
                        fhir_specimen_id = string(value=str(uuid.uuid4()))
                        fhir_specimen.id = fhir_specimen_id
                        fhir_bundle_entry.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_specimen_id is None else fhir_specimen_id if isinstance(fhir_specimen_id, str) else fhir_specimen_id.value)))
                        fhir_specimen_patient_reference = malac.models.fhir.r4.Reference()
                        fhir_specimen.subject = fhir_specimen_patient_reference
                        fhir_patient_id = malac.models.fhir.r4.string()
                        if fhir_patient.id is not None:
                            fhir_patient_id = fhir_patient.id
                        else:
                            fhir_patient.id = fhir_patient_id
                        fhir_specimen_patient_reference.reference = string(value=('urn:uuid:' + ('' if fhir_patient_id is None else fhir_patient_id if isinstance(fhir_patient_id, str) else fhir_patient_id.value)))
                        fhir_specimen_patient_reference.type_ = uri(value='Patient')
                        fhir_diagnosticReport_specimen_reference = malac.models.fhir.r4.Reference()
                        fhir_diagnosticReport.specimen.append(fhir_diagnosticReport_specimen_reference)
                        fhir_specimen_id = malac.models.fhir.r4.string()
                        if fhir_specimen.id is not None:
                            fhir_specimen_id = fhir_specimen.id
                        else:
                            fhir_specimen.id = fhir_specimen_id
                        fhir_diagnosticReport_specimen_reference.reference = string(value=('urn:uuid:' + ('' if fhir_specimen_id is None else fhir_specimen_id if isinstance(fhir_specimen_id, str) else fhir_specimen_id.value)))
                        fhir_diagnosticReport_specimen_reference.type_ = uri(value='Specimen')
                        fhir_specimen_collection = malac.models.fhir.r4.Specimen_Collection()
                        if fhir_specimen.collection is not None:
                            fhir_specimen_collection = fhir_specimen.collection
                        else:
                            fhir_specimen.collection = fhir_specimen_collection
                        cda_effectiveTime = cda_procedure.effectiveTime
                        if cda_effectiveTime:
                            if fhirpath.single([bool([v2 for v1 in [cda_effectiveTime] for v2 in fhirpath_utils.get(v1,'value')])]):
                                v = cda_effectiveTime.value
                                if v:
                                    fhir_specimen_collection.collectedDateTime = dateTime(value=dateutil.parser.parse(v).isoformat())
                        for targetSiteCode in cda_procedure.targetSiteCode or []:
                            fhir_specimen_collection.bodySite = malac.models.fhir.r4.CodeableConcept()
                            CDCodeableConcept(targetSiteCode, fhir_specimen_collection.bodySite)
                        for cda_participant in cda_procedure.participant or []:
                            cda_participantRole = cda_participant.participantRole
                            if cda_participantRole:
                                cda_playingEntity = cda_participantRole.playingEntity
                                if cda_playingEntity:
                                    for id_ in cda_participantRole.id or []:
                                        fhir_specimen.accessionIdentifier = malac.models.fhir.r4.Identifier()
                                        II(id_, fhir_specimen.accessionIdentifier)
                                    if cda_playingEntity.code:
                                        fhir_specimen.type_ = malac.models.fhir.r4.CodeableConcept()
                                        transform_default(cda_playingEntity.code, fhir_specimen.type_)
                        for cda_entryRelationship in cda_procedure.entryRelationship or []:
                            cda_act = cda_entryRelationship.act
                            if cda_act:
                                cda_effectiveTime = cda_act.effectiveTime
                                if cda_effectiveTime:
                                    if fhirpath.single([bool([v2 for v1 in [cda_effectiveTime] for v2 in fhirpath_utils.get(v1,'value')])]):
                                        v = cda_effectiveTime.value
                                        if v:
                                            fhir_specimen.receivedTime = dateTime(value=dateutil.parser.parse(v).isoformat())

def CdaLaboratorySpecialtySectionToFhirSection(cda, cda_section, fhir_section, fhir_practitionerRole, fhir_patient, fhir_diagnosticReport, fhir_bundle):
    CdaSectionToFhirSection(cda_section, fhir_section, fhir_bundle)
    for cda_section_entry in cda_section.entry or []:
        cda_act = cda_section_entry.act
        if cda_act:
            for cda_entryRelationship in cda_act.entryRelationship or []:
                if fhirpath.single([v5 for v5 in [v4 for v3 in [v2 for v1 in [cda_entryRelationship] for v2 in fhirpath_utils.get(v1,'organizer')] for v4 in fhirpath_utils.get(v3,'templateId')] if fhirpath_utils.equals(fhirpath_utils.get(v5,'root'), '==', ['1.3.6.1.4.1.19376.1.3.1.4']) == [True]]):
                    cda_laboratory_battery_organizer = cda_entryRelationship.organizer
                    if cda_laboratory_battery_organizer:
                        fhir_bundle_entry = malac.models.fhir.r4.Bundle_Entry()
                        fhir_bundle.entry.append(fhir_bundle_entry)
                        fhir_observation = malac.models.fhir.r4.Observation()
                        fhir_bundle_entry.resource = malac.models.fhir.r4.ResourceContainer(Observation=fhir_observation)
                        fhir_observation_id = string(value=str(uuid.uuid4()))
                        fhir_observation.id = fhir_observation_id
                        fhir_bundle_entry.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_observation_id is None else fhir_observation_id if isinstance(fhir_observation_id, str) else fhir_observation_id.value)))
                        fhir_section_entry_reference = malac.models.fhir.r4.Reference()
                        fhir_section.entry.append(fhir_section_entry_reference)
                        fhir_section_entry_reference.reference = string(value=('urn:uuid:' + ('' if fhir_observation_id is None else fhir_observation_id if isinstance(fhir_observation_id, str) else fhir_observation_id.value)))
                        fhir_section_entry_reference.type_ = uri(value='Observation')
                        fhir_observation_meta = malac.models.fhir.r4.Meta()
                        if fhir_observation.meta is not None:
                            fhir_observation_meta = fhir_observation.meta
                        else:
                            fhir_observation.meta = fhir_observation_meta
                        fhir_observation_meta.profile.append(string(value='http://hl7.eu/fhir/laboratory/StructureDefinition/Observation-resultslab-eu-lab'))
                        fhir_category = malac.models.fhir.r4.CodeableConcept()
                        fhir_observation.category.append(fhir_category)
                        fhir_category_coding = malac.models.fhir.r4.Coding()
                        fhir_category.coding.append(fhir_category_coding)
                        fhir_category_coding.system = uri(value='http://terminology.hl7.org/CodeSystem/observation-category')
                        fhir_category_coding.code = string(value='laboratory')
                        fhir_observation_subject_reference = malac.models.fhir.r4.Reference()
                        fhir_observation.subject = fhir_observation_subject_reference
                        fhir_patient_id = malac.models.fhir.r4.string()
                        if fhir_patient.id is not None:
                            fhir_patient_id = fhir_patient.id
                        else:
                            fhir_patient.id = fhir_patient_id
                        fhir_observation_subject_reference.reference = string(value=('urn:uuid:' + ('' if fhir_patient_id is None else fhir_patient_id if isinstance(fhir_patient_id, str) else fhir_patient_id.value)))
                        if cda_laboratory_battery_organizer.code:
                            fhir_observation.category.append(malac.models.fhir.r4.CodeableConcept())
                            CDCodeableConcept(cda_laboratory_battery_organizer.code, fhir_observation.category[-1])
                        if cda_laboratory_battery_organizer.code:
                            fhir_observation.code = malac.models.fhir.r4.CodeableConcept()
                            CDCodeableConcept(cda_laboratory_battery_organizer.code, fhir_observation.code)
                        organizer_statusCode = cda_laboratory_battery_organizer.statusCode
                        if organizer_statusCode:
                            cda_code = organizer_statusCode.code
                            if cda_code:
                                fhir_observation.status = string(value=translate_single('act-status-2-observation-status', (cda_code if isinstance(cda_code, str) else cda_code.value), 'code'))
                        cda_effectiveTime = cda_laboratory_battery_organizer.effectiveTime
                        if cda_effectiveTime:
                            fhir_observation_effective = malac.models.fhir.r4.dateTime()
                            fhir_observation.effectiveDateTime = fhir_observation_effective
                            fhir_observation_effective_extenstion = malac.models.fhir.r4.Extension()
                            fhir_observation_effective.extension.append(fhir_observation_effective_extenstion)
                            fhir_observation_effective_extenstion.url = 'http://hl7.org/fhir/StructureDefinition/data-absent-reason'
                            fhir_observation_effective_extenstion_code = malac.models.fhir.r4.code()
                            fhir_observation_effective_extenstion.valueCode = fhir_observation_effective_extenstion_code
                            fhir_observation_effective_extenstion_code.value = 'not-applicable'
                            TSDateTime(cda_effectiveTime, fhir_observation_effective)
                        if fhirpath.single(fhirpath_utils.bool_not([bool([v2 for v1 in [cda_laboratory_battery_organizer] for v2 in fhirpath_utils.get(v1,'effectiveTime')])])):
                            fhir_observation_effective = malac.models.fhir.r4.dateTime()
                            fhir_observation.effectiveDateTime = fhir_observation_effective
                            fhir_observation_effective.value = '1900-01-01'
                            fhir_observation_effective_extenstion = malac.models.fhir.r4.Extension()
                            fhir_observation_effective.extension.append(fhir_observation_effective_extenstion)
                            fhir_observation_effective_extenstion.url = 'http://hl7.org/fhir/StructureDefinition/data-absent-reason'
                            fhir_observation_effective_extenstion_code = malac.models.fhir.r4.code()
                            fhir_observation_effective_extenstion.valueCode = fhir_observation_effective_extenstion_code
                            fhir_observation_effective_extenstion_code.value = 'not-applicable'
                        for cda_laboratory_battery_organizer_performer in cda_laboratory_battery_organizer.performer:
                            if fhirpath.single([bool([v2 for v1 in [cda_laboratory_battery_organizer] for v2 in fhirpath_utils.get(v1,'performer')])]):
                                CdaPerformerToFhirObservationPerformer(cda_laboratory_battery_organizer_performer, fhir_observation, fhir_bundle)
                        if fhirpath.single(fhirpath_utils.bool_not([bool([v2 for v1 in [cda_laboratory_battery_organizer] for v2 in fhirpath_utils.get(v1,'performer')])])):
                            if fhirpath.single([bool([v6 for v5 in [v4 for v3 in fhirpath_utils.at_index([v2 for v1 in [cda] for v2 in fhirpath_utils.get(v1,'documentationOf')], [0]) for v4 in fhirpath_utils.get(v3,'serviceEvent')] for v6 in fhirpath_utils.get(v5,'performer')])]):
                                if len(cda.documentationOf) > 0:
                                    cda_documentationOf = cda.documentationOf[0]
                                    cda_documentationOf_serviceEvent = cda_documentationOf.serviceEvent
                                    if cda_documentationOf_serviceEvent:
                                        for cda_documentationOf_serviceEvent_performer in cda_documentationOf_serviceEvent.performer or []:
                                            if cda_documentationOf_serviceEvent_performer.time:
                                                fhir_observation.issued = malac.models.fhir.r4.instant()
                                                transform_default(cda_documentationOf_serviceEvent_performer.time, fhir_observation.issued)
                            fhir_observation_performer_reference = malac.models.fhir.r4.Reference()
                            fhir_observation.performer.append(fhir_observation_performer_reference)
                            fhir_practitionerRole_id = malac.models.fhir.r4.string()
                            if fhir_practitionerRole.id is not None:
                                fhir_practitionerRole_id = fhir_practitionerRole.id
                            else:
                                fhir_practitionerRole.id = fhir_practitionerRole_id
                            fhir_observation_performer_reference.reference = string(value=('urn:uuid:' + ('' if fhir_practitionerRole_id is None else fhir_practitionerRole_id if isinstance(fhir_practitionerRole_id, str) else fhir_practitionerRole_id.value)))
                            fhir_observation_performer_reference.type_ = uri(value='PractitionerRole')
                        for cda_component in cda_laboratory_battery_organizer.component or []:
                            if fhirpath.single([v5 for v5 in [v4 for v3 in [v2 for v1 in [cda_component] for v2 in fhirpath_utils.get(v1,'observation')] for v4 in fhirpath_utils.get(v3,'templateId')] if fhirpath_utils.equals(fhirpath_utils.get(v5,'root'), '==', ['1.3.6.1.4.1.19376.1.3.1.6']) == [True]]):
                                cda_laboratory_observation = cda_component.observation
                                if cda_laboratory_observation:
                                    fhir_bundle_entry = malac.models.fhir.r4.Bundle_Entry()
                                    fhir_bundle.entry.append(fhir_bundle_entry)
                                    fhir_laboratory_observation = malac.models.fhir.r4.Observation()
                                    fhir_bundle_entry.resource = malac.models.fhir.r4.ResourceContainer(Observation=fhir_laboratory_observation)
                                    fhir_laboratory_observation_id = string(value=str(uuid.uuid4()))
                                    fhir_laboratory_observation.id = fhir_laboratory_observation_id
                                    fhir_bundle_entry.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_laboratory_observation_id is None else fhir_laboratory_observation_id if isinstance(fhir_laboratory_observation_id, str) else fhir_laboratory_observation_id.value)))
                                    fhir_observation_hasMember_reference = malac.models.fhir.r4.Reference()
                                    fhir_observation.hasMember.append(fhir_observation_hasMember_reference)
                                    fhir_observation_hasMember_reference.reference = string(value=('urn:uuid:' + ('' if fhir_laboratory_observation_id is None else fhir_laboratory_observation_id if isinstance(fhir_laboratory_observation_id, str) else fhir_laboratory_observation_id.value)))
                                    fhir_observation_hasMember_reference.type_ = uri(value='Observation')
                                    CdaLaboratoryObservationToFhirObservation(cda, cda_laboratory_observation, fhir_laboratory_observation, fhir_practitionerRole, fhir_patient, fhir_bundle)

def CdaBeilagenSectionToFhirDiagnosticReportMedia(cda_section, fhir_diagnosticReport, fhir_bundle, fhir_patient):
    fhir_bundle_entry_01 = malac.models.fhir.r4.Bundle_Entry()
    fhir_bundle.entry.append(fhir_bundle_entry_01)
    fhir_media = malac.models.fhir.r4.Media()
    fhir_bundle_entry_01.resource = malac.models.fhir.r4.ResourceContainer(Media=fhir_media)
    fhir_media_id = string(value=str(uuid.uuid4()))
    fhir_media.id = fhir_media_id
    fhir_bundle_entry_01.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_media_id is None else fhir_media_id if isinstance(fhir_media_id, str) else fhir_media_id.value)))
    fhir_diagnosticReport_media = malac.models.fhir.r4.DiagnosticReport_Media()
    fhir_diagnosticReport.media.append(fhir_diagnosticReport_media)
    fhir_diagnosticReport_media_link_reference = malac.models.fhir.r4.Reference()
    fhir_diagnosticReport_media.link = fhir_diagnosticReport_media_link_reference
    fhir_diagnosticReport_media_link_reference.reference = string(value=('urn:uuid:' + ('' if fhir_media_id is None else fhir_media_id if isinstance(fhir_media_id, str) else fhir_media_id.value)))
    fhir_diagnosticReport_media_link_reference.type_ = uri(value='Media')
    for cda_section_entry in cda_section.entry or []:
        cda_observationMedia = cda_section_entry.observationMedia
        if cda_observationMedia:
            cda_section_text = cda_section.text
            if cda_section_text:
                fhir_diagnosticReport_media.comment = string(value=str(fhirpath.single([cda_section_text])))
            cda_observationMedia_ID = cda_observationMedia.ID
            if cda_observationMedia_ID:
                fhir_media_identifier = malac.models.fhir.r4.Identifier()
                fhir_media.identifier.append(fhir_media_identifier)
                fhir_media_identifier.value = string(value=cda_observationMedia_ID)
            fhir_media.status = string(value='completed')
            cda_observationMedia_value = cda_observationMedia.value
            if cda_observationMedia_value:
                fhir_media_content = malac.models.fhir.r4.Attachment()
                if fhir_media.content is not None:
                    fhir_media_content = fhir_media.content
                else:
                    fhir_media.content = fhir_media_content
                cda_mediaType = cda_observationMedia_value.mediaType
                if cda_mediaType:
                    fhir_media_content.contentType = string(value=cda_mediaType)
                fhir_media_content.data = base64Binary(value=fhirpath.single([v2 for v1 in [cda_observationMedia_value] for v2 in fhirpath_utils.get(v1,'valueOf_',strip=True)]))

def CdaBefundbewertungSectionToFhirSection(cda_section, fhir_section, fhir_bundle):
    CdaSectionToFhirSection(cda_section, fhir_section, fhir_bundle)
    fhir_section_code = malac.models.fhir.r4.CodeableConcept()
    if fhir_section.code is not None:
        fhir_section_code = fhir_section.code
    else:
        fhir_section.code = fhir_section_code
    fhir_section_coding = malac.models.fhir.r4.Coding()
    fhir_section_code.coding.append(fhir_section_coding)
    fhir_section_coding.code = string(value='48767-8')
    fhir_section_coding.system = uri(value='http://loinc.org')

def CdaZusammenfassungBehandlungSectionToFhir(cda_section, fhir_section, fhir_bundle):
    CdaSectionToFhirSection(cda_section, fhir_section, fhir_bundle)
    for cda_section_component in cda_section.component or []:
        cda_section_component_section = cda_section_component.section
        if cda_section_component_section:
            if fhirpath.single([v1 for v1 in fhirpath_utils.get(cda_section_component_section,'templateId') if fhirpath_utils.equals(fhirpath_utils.get(v1,'root'), '==', ['1.2.40.0.34.6.0.11.2.92']) == [True]]):
                fhir_section_section = malac.models.fhir.r4.Composition_Section()
                fhir_section.section.append(fhir_section_section)
                CdaSectionToFhirSection(cda_section_component_section, fhir_section_section, fhir_bundle)

def CdaAuszugErhobeneDatenSectionToFhir(cda_section, fhir_section, fhir_bundle):
    CdaSectionToFhirSection(cda_section, fhir_section, fhir_bundle)
    for cda_section_component in cda_section.component or []:
        cda_section_component_section = cda_section_component.section
        if cda_section_component_section:
            if fhirpath.single([v1 for v1 in fhirpath_utils.get(cda_section_component_section,'templateId') if fhirpath_utils.equals(fhirpath_utils.get(v1,'root'), '==', ['1.2.40.0.34.6.0.11.2.92']) == [True]]):
                fhir_section_section = malac.models.fhir.r4.Composition_Section()
                fhir_section.section.append(fhir_section_section)
                CdaSectionToFhirSection(cda_section_component_section, fhir_section_section, fhir_bundle)

def CdaDiagnosisToFhirSection(cda, cda_section, fhir_section, fhir_practitionerRole, fhir_patient, fhir_diagnosticReport, fhir_bundle):
    CdaSectionToFhirSection(cda_section, fhir_section, fhir_bundle)

def CdaObservationToFhirObservation(cda_observation, fhir_observation):
    for id_ in cda_observation.id or []:
        fhir_observation.identifier.append(malac.models.fhir.r4.Identifier())
        II(id_, fhir_observation.identifier[-1])

def CdaLaboratoryObservationToFhirObservation(cda, cda_laboratory_observation, fhir_observation, fhir_practitionerRole, fhir_patient, fhir_bundle):
    fhir_observation_meta = malac.models.fhir.r4.Meta()
    if fhir_observation.meta is not None:
        fhir_observation_meta = fhir_observation.meta
    else:
        fhir_observation.meta = fhir_observation_meta
    fhir_observation_meta.profile.append(string(value='http://hl7.eu/fhir/laboratory/StructureDefinition/Observation-resultslab-eu-lab'))
    for id_ in cda_laboratory_observation.id or []:
        fhir_observation.identifier.append(malac.models.fhir.r4.Identifier())
        II(id_, fhir_observation.identifier[-1])
    fhir_category = malac.models.fhir.r4.CodeableConcept()
    fhir_observation.category.append(fhir_category)
    fhir_category_coding = malac.models.fhir.r4.Coding()
    fhir_category.coding.append(fhir_category_coding)
    fhir_category_coding.system = uri(value='http://terminology.hl7.org/CodeSystem/observation-category')
    fhir_category_coding.code = string(value='laboratory')
    fhir_observation_subject_reference = malac.models.fhir.r4.Reference()
    fhir_observation.subject = fhir_observation_subject_reference
    fhir_patient_id = malac.models.fhir.r4.string()
    if fhir_patient.id is not None:
        fhir_patient_id = fhir_patient.id
    else:
        fhir_patient.id = fhir_patient_id
    fhir_observation_subject_reference.reference = string(value=('urn:uuid:' + ('' if fhir_patient_id is None else fhir_patient_id if isinstance(fhir_patient_id, str) else fhir_patient_id.value)))
    if cda_laboratory_observation.code:
        fhir_observation.code = malac.models.fhir.r4.CodeableConcept()
        CDCodeableConcept(cda_laboratory_observation.code, fhir_observation.code)
    if fhirpath.single(fhirpath_utils.bool_not([bool([v3 for v3 in [v2 for v1 in [cda_laboratory_observation] for v2 in fhirpath_utils.get(v1,'value')] if fhirpath_utils.bool_and(fhirpath_utils.equals(fhirpath_utils.get(v3,'code'), '==', ['255599008']), fhirpath_utils.equals(fhirpath_utils.get(v3,'codeSystem'), '==', ['2.16.840.1.113883.6.96'])) == [True]])])):
        observation_statusCode = cda_laboratory_observation.statusCode
        if observation_statusCode:
            cda_code = observation_statusCode.code
            if cda_code:
                fhir_observation.status = string(value=translate_single('act-status-2-observation-status', (cda_code if isinstance(cda_code, str) else cda_code.value), 'code'))
    if fhirpath.single([bool([v3 for v3 in [v2 for v1 in [cda_laboratory_observation] for v2 in fhirpath_utils.get(v1,'value')] if fhirpath_utils.bool_and(fhirpath_utils.equals(fhirpath_utils.get(v3,'code'), '==', ['255599008']), fhirpath_utils.equals(fhirpath_utils.get(v3,'codeSystem'), '==', ['2.16.840.1.113883.6.96'])) == [True]])]):
        fhir_observation.status = string(value='preliminary')
        fhir_observation_dataAbsentReason = malac.models.fhir.r4.CodeableConcept()
        if fhir_observation.dataAbsentReason is not None:
            fhir_observation_dataAbsentReason = fhir_observation.dataAbsentReason
        else:
            fhir_observation.dataAbsentReason = fhir_observation_dataAbsentReason
        fhir_observation_dataAbsentReason_coding = malac.models.fhir.r4.Coding()
        fhir_observation_dataAbsentReason.coding.append(fhir_observation_dataAbsentReason_coding)
        fhir_observation_dataAbsentReason_coding.code = string(value='temp-unknown')
        fhir_observation_dataAbsentReason_coding.system = uri(value='http://terminology.hl7.org/CodeSystem/data-absent-reason')
    cda_effectiveTime = cda_laboratory_observation.effectiveTime
    if cda_effectiveTime:
        fhir_observation_effective = malac.models.fhir.r4.dateTime()
        fhir_observation.effectiveDateTime = fhir_observation_effective
        TSDateTime(cda_effectiveTime, fhir_observation_effective)
    if fhirpath.single([v3 for v3 in [v2 for v1 in [cda_laboratory_observation] for v2 in fhirpath_utils.get(v1,'effectiveTime')] if fhirpath_utils.equals(fhirpath_utils.get(v3,'nullFlavor'), '==', ['UNK']) == [True]]):
        fhir_observation_effective = malac.models.fhir.r4.dateTime()
        fhir_observation.effectiveDateTime = fhir_observation_effective
        fhir_observation_effective_extenstion = malac.models.fhir.r4.Extension()
        fhir_observation_effective.extension.append(fhir_observation_effective_extenstion)
        fhir_observation_effective_extenstion.url = 'http://hl7.org/fhir/StructureDefinition/data-absent-reason'
        fhir_observation_effective_extenstion_code = malac.models.fhir.r4.code()
        fhir_observation_effective_extenstion.valueCode = fhir_observation_effective_extenstion_code
        fhir_observation_effective_extenstion_code.value = 'unknown'
    for cda_observation_value in cda_laboratory_observation.value or []:
        if isinstance(cda_observation_value, malac.models.cda.at_ext.PQ):
            fhir_observation_value = malac.models.fhir.r4.Quantity()
            fhir_observation.valueQuantity = fhir_observation_value
            PQQuantity(cda_observation_value, fhir_observation_value)
    for cda_observation_value in cda_laboratory_observation.value or []:
        if isinstance(cda_observation_value, malac.models.cda.at_ext.IVL_PQ):
            fhir_observation_value = malac.models.fhir.r4.Range()
            fhir_observation.valueRange = fhir_observation_value
            IVLPQRange(cda_observation_value, fhir_observation_value)
    if fhirpath.single(fhirpath_utils.bool_not([bool([v3 for v3 in [v2 for v1 in [cda_laboratory_observation] for v2 in fhirpath_utils.get(v1,'value')] if fhirpath_utils.bool_and(fhirpath_utils.equals(fhirpath_utils.get(v3,'code'), '==', ['255599008']), fhirpath_utils.equals(fhirpath_utils.get(v3,'codeSystem'), '==', ['2.16.840.1.113883.6.96'])) == [True]])])):
        for cda_observation_value in cda_laboratory_observation.value or []:
            if isinstance(cda_observation_value, malac.models.cda.at_ext.CD):
                fhir_observation_value = malac.models.fhir.r4.CodeableConcept()
                fhir_observation.valueCodeableConcept = fhir_observation_value
                CDCodeableConcept(cda_observation_value, fhir_observation_value)
    for cda_observation_value in cda_laboratory_observation.value or []:
        if isinstance(cda_observation_value, malac.models.cda.at_ext.ST):
            fhir_observation_value = malac.models.fhir.r4.string()
            fhir_observation.valueString = fhir_observation_value
            STstring(cda_observation_value, fhir_observation_value)
    for interpretationCode in cda_laboratory_observation.interpretationCode or []:
        fhir_observation.interpretation.append(malac.models.fhir.r4.CodeableConcept())
        transform_default(interpretationCode, fhir_observation.interpretation[-1])
    for cda_laboratory_observation_performer in cda_laboratory_observation.performer:
        if fhirpath.single([bool([v2 for v1 in [cda_laboratory_observation] for v2 in fhirpath_utils.get(v1,'performer')])]):
            CdaPerformerToFhirObservationPerformer(cda_laboratory_observation_performer, fhir_observation, fhir_bundle)
    if fhirpath.single(fhirpath_utils.bool_not([bool([v2 for v1 in [cda_laboratory_observation] for v2 in fhirpath_utils.get(v1,'performer')])])):
        if fhirpath.single([bool([v6 for v5 in [v4 for v3 in fhirpath_utils.at_index([v2 for v1 in [cda] for v2 in fhirpath_utils.get(v1,'documentationOf')], [0]) for v4 in fhirpath_utils.get(v3,'serviceEvent')] for v6 in fhirpath_utils.get(v5,'performer')])]):
            if len(cda.documentationOf) > 0:
                cda_documentationOf = cda.documentationOf[0]
                cda_documentationOf_serviceEvent = cda_documentationOf.serviceEvent
                if cda_documentationOf_serviceEvent:
                    for cda_documentationOf_serviceEvent_performer in cda_documentationOf_serviceEvent.performer or []:
                        if cda_documentationOf_serviceEvent_performer.time:
                            fhir_observation.issued = malac.models.fhir.r4.instant()
                            transform_default(cda_documentationOf_serviceEvent_performer.time, fhir_observation.issued)
        fhir_observation_performer_reference = malac.models.fhir.r4.Reference()
        fhir_observation.performer.append(fhir_observation_performer_reference)
        fhir_practitionerRole_id = malac.models.fhir.r4.string()
        if fhir_practitionerRole.id is not None:
            fhir_practitionerRole_id = fhir_practitionerRole.id
        else:
            fhir_practitionerRole.id = fhir_practitionerRole_id
        fhir_observation_performer_reference.reference = string(value=('urn:uuid:' + ('' if fhir_practitionerRole_id is None else fhir_practitionerRole_id if isinstance(fhir_practitionerRole_id, str) else fhir_practitionerRole_id.value)))
        fhir_observation_performer_reference.type_ = uri(value='PractitionerRole')
    for cda_observation_referenceRange in cda_laboratory_observation.referenceRange or []:
        cda_referenceRange_observationRange = cda_observation_referenceRange.observationRange
        if cda_referenceRange_observationRange:
            fhir_observation_referenceRange = malac.models.fhir.r4.Observation_ReferenceRange()
            fhir_observation.referenceRange.append(fhir_observation_referenceRange)
            if cda_referenceRange_observationRange.text:
                fhir_observation_referenceRange.text = malac.models.fhir.r4.string()
                EDstring(cda_referenceRange_observationRange.text, fhir_observation_referenceRange.text)
            cda_observationRange_value = cda_referenceRange_observationRange.value
            if cda_observationRange_value:
                for low in (cda_observationRange_value.low if isinstance(cda_observationRange_value.low, list) else ([] if not cda_observationRange_value.low else [cda_observationRange_value.low])):
                    fhir_observation_referenceRange.low = malac.models.fhir.r4.Quantity()
                    transform_default(low, fhir_observation_referenceRange.low)
                for high in (cda_observationRange_value.high if isinstance(cda_observationRange_value.high, list) else ([] if not cda_observationRange_value.high else [cda_observationRange_value.high])):
                    fhir_observation_referenceRange.high = malac.models.fhir.r4.Quantity()
                    transform_default(high, fhir_observation_referenceRange.high)
            fhir_referenceRange_type = malac.models.fhir.r4.CodeableConcept()
            if fhir_observation_referenceRange.type_ is not None:
                fhir_referenceRange_type = fhir_observation_referenceRange.type_
            else:
                fhir_observation_referenceRange.type_ = fhir_referenceRange_type
            fhir_type_coding = malac.models.fhir.r4.Coding()
            fhir_referenceRange_type.coding.append(fhir_type_coding)
            fhir_type_coding.system = uri(value='http://terminology.hl7.org/CodeSystem/referencerange-meaning')
            fhir_type_coding.code = string(value='normal')

def CdaAssignedEntityToFhirPractitionerRole(cda_assignedEntity, fhir_practitionerRole, fhir_bundle):
    fhir_bundle_entry = malac.models.fhir.r4.Bundle_Entry()
    fhir_bundle.entry.append(fhir_bundle_entry)
    fhir_practitioner = malac.models.fhir.r4.Practitioner()
    fhir_bundle_entry.resource = malac.models.fhir.r4.ResourceContainer(Practitioner=fhir_practitioner)
    fhir_practitioner_id = string(value=str(uuid.uuid4()))
    fhir_practitioner.id = fhir_practitioner_id
    fhir_bundle_entry.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_practitioner_id is None else fhir_practitioner_id if isinstance(fhir_practitioner_id, str) else fhir_practitioner_id.value)))
    fhir_practitionerRole_practitioner_reference = malac.models.fhir.r4.Reference()
    fhir_practitionerRole.practitioner = fhir_practitionerRole_practitioner_reference
    fhir_practitionerRole_practitioner_reference.reference = string(value=('urn:uuid:' + ('' if fhir_practitioner_id is None else fhir_practitioner_id if isinstance(fhir_practitioner_id, str) else fhir_practitioner_id.value)))
    fhir_practitionerRole_practitioner_reference.type_ = uri(value='Practitioner')
    for id_ in cda_assignedEntity.id or []:
        fhir_practitionerRole.identifier.append(malac.models.fhir.r4.Identifier())
        II(id_, fhir_practitionerRole.identifier[-1])
    if cda_assignedEntity.code:
        fhir_practitionerRole.code.append(malac.models.fhir.r4.CodeableConcept())
        transform_default(cda_assignedEntity.code, fhir_practitionerRole.code[-1])
    for addr in cda_assignedEntity.addr or []:
        fhir_practitioner.address.append(malac.models.fhir.r4.Address())
        CdaAdressCompilationToFhirAustrianAddress(addr, fhir_practitioner.address[-1])
    for telecom in cda_assignedEntity.telecom or []:
        fhir_practitioner.telecom.append(malac.models.fhir.r4.ContactPoint())
        TELContactPoint(telecom, fhir_practitioner.telecom[-1])
    cda_assignedPerson = cda_assignedEntity.assignedPerson
    if cda_assignedPerson:
        for name in cda_assignedPerson.name or []:
            fhir_practitioner.name.append(malac.models.fhir.r4.HumanName())
            CdaPersonNameCompilationToFhirHumanName(name, fhir_practitioner.name[-1])
    cda_representedOrganization = cda_assignedEntity.representedOrganization
    if cda_representedOrganization:
        fhir_bundle_entry = malac.models.fhir.r4.Bundle_Entry()
        fhir_bundle.entry.append(fhir_bundle_entry)
        fhir_organization = malac.models.fhir.r4.Organization()
        fhir_bundle_entry.resource = malac.models.fhir.r4.ResourceContainer(Organization=fhir_organization)
        fhir_organization_id = string(value=str(uuid.uuid4()))
        fhir_organization.id = fhir_organization_id
        fhir_bundle_entry.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_organization_id is None else fhir_organization_id if isinstance(fhir_organization_id, str) else fhir_organization_id.value)))
        fhir_practitionerRole_organization = malac.models.fhir.r4.Reference()
        fhir_practitionerRole.organization = fhir_practitionerRole_organization
        fhir_practitionerRole_organization.reference = string(value=('urn:uuid:' + ('' if fhir_organization_id is None else fhir_organization_id if isinstance(fhir_organization_id, str) else fhir_organization_id.value)))
        fhir_practitionerRole_organization.type_ = uri(value='Organization')
        CdaOrganizationCompilationToFhirOrganization(cda_representedOrganization, fhir_organization)

def CdaAssociatedEntityToFhirPractitionerRole(cda_associatedEntity, fhir_practitionerRole, fhir_bundle):
    fhir_bundle_entry = malac.models.fhir.r4.Bundle_Entry()
    fhir_bundle.entry.append(fhir_bundle_entry)
    fhir_practitioner = malac.models.fhir.r4.Practitioner()
    fhir_bundle_entry.resource = malac.models.fhir.r4.ResourceContainer(Practitioner=fhir_practitioner)
    fhir_practitioner_id = string(value=str(uuid.uuid4()))
    fhir_practitioner.id = fhir_practitioner_id
    fhir_bundle_entry.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_practitioner_id is None else fhir_practitioner_id if isinstance(fhir_practitioner_id, str) else fhir_practitioner_id.value)))
    fhir_practitionerRole_practitioner_reference = malac.models.fhir.r4.Reference()
    fhir_practitionerRole.practitioner = fhir_practitionerRole_practitioner_reference
    fhir_practitionerRole_practitioner_reference.reference = string(value=('urn:uuid:' + ('' if fhir_practitioner_id is None else fhir_practitioner_id if isinstance(fhir_practitioner_id, str) else fhir_practitioner_id.value)))
    fhir_practitionerRole_practitioner_reference.type_ = uri(value='Practitioner')
    for id_ in cda_associatedEntity.id or []:
        fhir_practitionerRole.identifier.append(malac.models.fhir.r4.Identifier())
        II(id_, fhir_practitionerRole.identifier[-1])
    for addr in cda_associatedEntity.addr or []:
        fhir_practitioner.address.append(malac.models.fhir.r4.Address())
        CdaAdressCompilationToFhirAustrianAddress(addr, fhir_practitioner.address[-1])
    for telecom in cda_associatedEntity.telecom or []:
        fhir_practitioner.telecom.append(malac.models.fhir.r4.ContactPoint())
        TELContactPoint(telecom, fhir_practitioner.telecom[-1])
    cda_associatedPerson = cda_associatedEntity.associatedPerson
    if cda_associatedPerson:
        for name in cda_associatedPerson.name or []:
            fhir_practitioner.name.append(malac.models.fhir.r4.HumanName())
            CdaPersonNameCompilationToFhirHumanName(name, fhir_practitioner.name[-1])
    cda_scopingOrganization = cda_associatedEntity.scopingOrganization
    if cda_scopingOrganization:
        fhir_bundle_entry = malac.models.fhir.r4.Bundle_Entry()
        fhir_bundle.entry.append(fhir_bundle_entry)
        fhir_organization = malac.models.fhir.r4.Organization()
        fhir_bundle_entry.resource = malac.models.fhir.r4.ResourceContainer(Organization=fhir_organization)
        fhir_organization_id = string(value=str(uuid.uuid4()))
        fhir_organization.id = fhir_organization_id
        fhir_bundle_entry.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_organization_id is None else fhir_organization_id if isinstance(fhir_organization_id, str) else fhir_organization_id.value)))
        fhir_practitionerRole_organization = malac.models.fhir.r4.Reference()
        fhir_practitionerRole.organization = fhir_practitionerRole_organization
        fhir_practitionerRole_organization.reference = string(value=('urn:uuid:' + ('' if fhir_organization_id is None else fhir_organization_id if isinstance(fhir_organization_id, str) else fhir_organization_id.value)))
        fhir_practitionerRole_organization.type_ = uri(value='Organization')
        CdaOrganizationCompilationToFhirOrganization(cda_scopingOrganization, fhir_organization)

def CdaPerformerToFhirObservationPerformer(cda_performer, fhir_observation, fhir_bundle):
    if cda_performer.time:
        fhir_observation.issued = malac.models.fhir.r4.instant()
        transform_default(cda_performer.time, fhir_observation.issued)
    cda_performer_assignedEntity = cda_performer.assignedEntity
    if cda_performer_assignedEntity:
        fhir_bundle_entry01 = malac.models.fhir.r4.Bundle_Entry()
        fhir_bundle.entry.append(fhir_bundle_entry01)
        fhir_practitionerRole = malac.models.fhir.r4.PractitionerRole()
        fhir_bundle_entry01.resource = malac.models.fhir.r4.ResourceContainer(PractitionerRole=fhir_practitionerRole)
        fhir_practitionerRole_id = string(value=str(uuid.uuid4()))
        fhir_practitionerRole.id = fhir_practitionerRole_id
        fhir_bundle_entry01.fullUrl = uri(value=('urn:uuid:' + ('' if fhir_practitionerRole_id is None else fhir_practitionerRole_id if isinstance(fhir_practitionerRole_id, str) else fhir_practitionerRole_id.value)))
        fhir_observation_performer_reference = malac.models.fhir.r4.Reference()
        fhir_observation.performer.append(fhir_observation_performer_reference)
        fhir_observation_performer_reference.reference = string(value=('urn:uuid:' + ('' if fhir_practitionerRole_id is None else fhir_practitionerRole_id if isinstance(fhir_practitionerRole_id, str) else fhir_practitionerRole_id.value)))
        fhir_observation_performer_reference.type_ = uri(value='PractitionerRole')
        CdaAssignedEntityToFhirPractitionerRole(cda_performer_assignedEntity, fhir_practitionerRole, fhir_bundle)

# output
# 1..1 result (boolean)
# 0..1 message with error details for human (string)
# 0..* match with (list)
#   0..1 equivalence/relationship
#   0..1 concept
#       0..1 system
#       0..1 version
#       0..1 code
#       0..1 display 
#       0..1 userSelected will always be false, because this is a translation
#   0..1 source (conceptMap url)
# TODO implement reverse
def translate(url=None, conceptMapVersion=None, code=None, system=None, version=None, source=None, coding=None, codeableConcept=None, target=None, targetsystem=None, reverse=None, silent=False)              -> dict [bool, str, list[dict[str, dict[str, str, str, str, bool], str]]]:
    start = time.time()
    
    # start validation and recall of translate in simple from
    if codeableConcept:
        if isinstance(codeableConcept, str): 
            codeableConcept = malac.models.fhir.r4.parseString(codeableConcept, silent)
        elif isinstance(coding, malac.models.fhir.r4.CodeableConcept):
            pass
        else:
            raise BaseException("The codeableConcept parameter has to be a string or a CodeableConcept Object (called method as library)!")
        # the first fit will be returned, else the last unfitted value will be returned
        # TODO check translate params
        for one_coding in codeableConcept.get_coding:
            if (ret := translate(url=url, source=source, coding=one_coding, 
                                 target=target, targetsystem=targetsystem, 
                                 reverse=reverse, silent=True))[0]:
                return ret
        else: return ret
    elif coding:
        if isinstance(coding, str): 
            coding = malac.models.fhir.r4.parseString(coding, silent)
        elif isinstance(coding, malac.models.fhir.r4.Coding):
            pass
        else:
            raise BaseException("The coding parameter has to be a string or a Coding Object (called method as library)!")
        # TODO check translate params
        return translate(url=url,  source=source, coding=one_coding, 
                         target=target, targetsystem=targetsystem, 
                         reverse=reverse, silent=True)
    elif code:
        if not isinstance(code,str): 
            raise BaseException("The code parameter has to be a string!")
    elif target:
        if not isinstance(code,str): 
            raise BaseException("The target parameter has to be a string!")
    elif targetsystem:
        if not isinstance(code,str): 
            raise BaseException("The targetsystem parameter has to be a string!")
    else:
        raise BaseException("At least codeableConcept, coding, code, target or targetSystem has to be given!")
    # end validation and recall of translate in simplier from

    # look for any information from the one ore more generated conceptMaps into conceptMap_as_7dimension_dict
    match = []
    unmapped = []
    if url and url not in conceptMap_as_7dimension_dict.keys():
        print('   #ERROR# ConceptMap with URL "'+ url +'" is not loaded to this compiled conceptMap #ERROR#')
    else:
        for url_lvl in conceptMap_as_7dimension_dict:
            if url_lvl == "%" or not url or url_lvl == str(url or ""):#+str(("/?version=" and conceptMapVersion) or ""):
                for source_lvl in conceptMap_as_7dimension_dict[url_lvl]:
                    if source_lvl == "%" or not source or source_lvl == source:
                        for target_lvl in conceptMap_as_7dimension_dict[url_lvl][source_lvl]:
                            if target_lvl == "%" or not target or target_lvl == target:
                                for system_lvl in conceptMap_as_7dimension_dict[url_lvl][source_lvl][target_lvl]:
                                    if system_lvl == "%" or not system or system_lvl == system:#+str(("/?version=" and version) or ""):
                                        for targetsystem_lvl in conceptMap_as_7dimension_dict[url_lvl][source_lvl][target_lvl][system_lvl]:
                                            if targetsystem_lvl == "%" or not targetsystem or targetsystem_lvl == targetsystem:
                                                for code_lvl in conceptMap_as_7dimension_dict[url_lvl][source_lvl][target_lvl][system_lvl][targetsystem_lvl]:
                                                    if code_lvl == "|" or code_lvl == "~" or code_lvl == "#":
                                                        unmapped += conceptMap_as_7dimension_dict[url_lvl][source_lvl][target_lvl][system_lvl][targetsystem_lvl][code_lvl]
                                                    if code_lvl == "%" or not code or code_lvl == code:
                                                        match += conceptMap_as_7dimension_dict[url_lvl][source_lvl][target_lvl][system_lvl][targetsystem_lvl][code_lvl]                
                                                    
    if not match:
        for one_unmapped in unmapped:
            tmp_system = ""
            tmp_version = ""
            tmp_code = ""
            tmp_display = ""
            # replace all "|" values with to translated code (provided from https://hl7.org/fhir/R4B/conceptmap-definitions.html#ConceptMap.group.unmapped.mode)
            if one_unmapped["concept"]["code"].startswith("|"):
                tmp_system = system
                tmp_version = version
                tmp_code = one_unmapped["concept"]["code"][1:] + code
            # replace all "~" values with fixed code (provided from https://hl7.org/fhir/R4B/conceptmap-definitions.html#ConceptMap.group.unmapped.mode)
            elif one_unmapped["concept"]["code"].startswith("~"):
                if tmp := one_unmapped["concept"]["system"]: tmp_system = tmp 
                tmp_code = one_unmapped["concept"]["code"][1:]
                tmp_display = one_unmapped["concept"]["display"]
            elif one_unmapped["concept"]["code"].startswith("#"):
                # TODO detect recursion like conceptMapA -> conceptMapB -> ConceptMapA -> ...
                return translate(one_unmapped["concept"]["code"][1:], None, code, system, version, source, 
                                 coding, codeableConcept, target, targetsystem, reverse, silent)
            # prepare the match.concept results
            concept = {}
            if tmp_system: concept["system"] = tmp_system
            if tmp_version: concept["version"] = tmp_version
            if tmp_code: concept["code"] = tmp_code
            if tmp_display: concept["display"] = tmp_display

            # if the concept dict is empty, than skip this broken value and give a warning, that there is a empty group
            if concept == {}:
                # TODO do a warning, that it seems like the conceptmap is broken, because there is a empty group
                continue
            
            match.append({"relationship": one_unmapped["relationship"], 
                          "concept": concept,
                          "source": one_unmapped["source"]})

    # see if any match is not in R4 "unmatched" or "disjoint" and in R5 "not-related-to"
    result = False
    message = ""
    for one_match in match:
        if one_match["relationship"] not in ['not-related-to']:
            result = True 
            # for printing only, if no url was initially given use the conceptmap
            if not url:
                url = one_match["source"]

    if not silent:
        print('Translation in '+str(round(time.time()-start,3))+' seconds for code "'+(code or "NONE")+'" with ConceptMap "'+url+'"')
    return {"result": result, "message": message, "match": match}

conceptMap_as_7dimension_dict = {}


conceptMap_as_7dimension_dict["cda-code-2-fhir-category"] = {
    "%": {
        "%": {
            "http://loinc.org": {
                "http://loinc.org": {
                    "11502-2": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://loinc.org",
                                "code": "26436-6"
                            },
                            "source": "cda-code-2-fhir-category"
                        }
                    ],
                    "18725-2": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://loinc.org",
                                "code": "18725-2"
                            },
                            "source": "cda-code-2-fhir-category"
                        }
                    ],
                    "75498-6": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://loinc.org",
                                "code": "75498-6"
                            },
                            "source": "cda-code-2-fhir-category"
                        }
                    ],
                    "75496-0": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://loinc.org",
                                "code": "75496-0"
                            },
                            "source": "cda-code-2-fhir-category"
                        }
                    ]
                }
            }
        }
    }
}

conceptMap_as_7dimension_dict["cda-sdtc-statuscode-2-fhir-composition-status"] = {
    "%": {
        "%": {
            "http://hl7.org/fhir/ValueSet/composition-status": {
                "http://hl7.org/fhir/ValueSet/composition-status": {
                    "active": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://hl7.org/fhir/ValueSet/composition-status",
                                "code": "preliminary"
                            },
                            "source": "cda-sdtc-statuscode-2-fhir-composition-status"
                        }
                    ],
                    "nullified": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://hl7.org/fhir/ValueSet/composition-status",
                                "code": "entered-in-error"
                            },
                            "source": "cda-sdtc-statuscode-2-fhir-composition-status"
                        }
                    ]
                }
            }
        }
    }
}

conceptMap_as_7dimension_dict["cm-v3-administrative-gender"] = {
    "%": {
        "%": {
            "http://terminology.hl7.org/ValueSet/v3-AdministrativeGender": {
                "http://hl7.org/fhir/ValueSet/administrative-gender": {
                    "M": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://terminology.hl7.org/ValueSet/v3-AdministrativeGender",
                                "code": "male"
                            },
                            "source": "cm-v3-administrative-gender"
                        }
                    ],
                    "F": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://terminology.hl7.org/ValueSet/v3-AdministrativeGender",
                                "code": "female"
                            },
                            "source": "cm-v3-administrative-gender"
                        }
                    ]
                }
            }
        }
    }
}

conceptMap_as_7dimension_dict["ELGAAdministrativeGenderFHIRGender"] = {
    "%": {
        "%": {
            "https://termgit.elga.gv.at/ValueSet-elga-administrativegender": {
                "http://hl7.org/fhir/ValueSet/administrative-gender": {
                    "F": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-administrativegender",
                                "code": "female"
                            },
                            "source": "ELGAAdministrativeGenderFHIRGender"
                        }
                    ],
                    "M": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-administrativegender",
                                "code": "male"
                            },
                            "source": "ELGAAdministrativeGenderFHIRGender"
                        }
                    ],
                    "UN": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-administrativegender",
                                "code": "other"
                            },
                            "source": "ELGAAdministrativeGenderFHIRGender"
                        }
                    ]
                }
            }
        }
    }
}

conceptMap_as_7dimension_dict["act-status-2-observation-status"] = {
    "%": {
        "%": {
            "http://terminology.hl7.org/ValueSet/v3-ActStatus": {
                "http://hl7.org/fhir/ValueSet/observation-status": {
                    "completed": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://terminology.hl7.org/ValueSet/v3-ActStatus",
                                "code": "final"
                            },
                            "source": "act-status-2-observation-status"
                        }
                    ],
                    "active": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://terminology.hl7.org/ValueSet/v3-ActStatus",
                                "code": "preliminary"
                            },
                            "source": "act-status-2-observation-status"
                        }
                    ],
                    "aborted": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://terminology.hl7.org/ValueSet/v3-ActStatus",
                                "code": "cancelled"
                            },
                            "source": "act-status-2-observation-status"
                        }
                    ]
                }
            }
        }
    }
}

conceptMap_as_7dimension_dict["addressUse"] = {
    "%": {
        "%": {
            "http://terminology.hl7.org/ValueSet/v3-AddressUse": {
                "http://hl7.org/fhir/valueset-address-use.html": {
                    "H": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://terminology.hl7.org/ValueSet/v3-AddressUse",
                                "code": "home"
                            },
                            "source": "addressUse"
                        }
                    ],
                    "HP": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://terminology.hl7.org/ValueSet/v3-AddressUse",
                                "code": "home"
                            },
                            "source": "addressUse"
                        }
                    ],
                    "HV": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://terminology.hl7.org/ValueSet/v3-AddressUse",
                                "code": "home"
                            },
                            "source": "addressUse"
                        }
                    ],
                    "WP": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://terminology.hl7.org/ValueSet/v3-AddressUse",
                                "code": "work"
                            },
                            "source": "addressUse"
                        }
                    ],
                    "DIR": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://terminology.hl7.org/ValueSet/v3-AddressUse",
                                "code": "work"
                            },
                            "source": "addressUse"
                        }
                    ],
                    "PUB": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://terminology.hl7.org/ValueSet/v3-AddressUse",
                                "code": "work"
                            },
                            "source": "addressUse"
                        }
                    ],
                    "TMP": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://terminology.hl7.org/ValueSet/v3-AddressUse",
                                "code": "temp"
                            },
                            "source": "addressUse"
                        }
                    ],
                    "OLD": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://terminology.hl7.org/ValueSet/v3-AddressUse",
                                "code": "old"
                            },
                            "source": "addressUse"
                        }
                    ],
                    "BAD": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://terminology.hl7.org/ValueSet/v3-AddressUse",
                                "code": "old"
                            },
                            "source": "addressUse"
                        }
                    ]
                }
            }
        }
    }
}

conceptMap_as_7dimension_dict["ELGA2FHIRAddressUse"] = {
    "%": {
        "%": {
            "https://termgit.elga.gv.at/ValueSet/elga-addressuse": {
                "http://hl7.org/fhir/ValueSet/address-use": {
                    "H": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet/elga-addressuse",
                                "code": "home"
                            },
                            "source": "ELGA2FHIRAddressUse"
                        }
                    ],
                    "HP": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet/elga-addressuse",
                                "code": "home"
                            },
                            "source": "ELGA2FHIRAddressUse"
                        }
                    ],
                    "HV": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet/elga-addressuse",
                                "code": "home"
                            },
                            "source": "ELGA2FHIRAddressUse"
                        }
                    ],
                    "WP": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet/elga-addressuse",
                                "code": "work"
                            },
                            "source": "ELGA2FHIRAddressUse"
                        }
                    ],
                    "DIR": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet/elga-addressuse",
                                "code": "work"
                            },
                            "source": "ELGA2FHIRAddressUse"
                        }
                    ],
                    "PUB": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet/elga-addressuse",
                                "code": "work"
                            },
                            "source": "ELGA2FHIRAddressUse"
                        }
                    ],
                    "TMP": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet/elga-addressuse",
                                "code": "temp"
                            },
                            "source": "ELGA2FHIRAddressUse"
                        }
                    ],
                    "PHYS": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet/elga-addressuse",
                                "code": "home"
                            },
                            "source": "ELGA2FHIRAddressUse"
                        }
                    ],
                    "PST": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet/elga-addressuse",
                                "code": "home"
                            },
                            "source": "ELGA2FHIRAddressUse"
                        }
                    ]
                }
            }
        }
    }
}

conceptMap_as_7dimension_dict["ELGATelecomAddressUseFHIRContactPointUse"] = {
    "%": {
        "%": {
            "https://termgit.elga.gv.at/ValueSet-elga-telecomaddressuse": {
                "http://hl7.org/fhir/ValueSet/contact-point-use": {
                    "H": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-telecomaddressuse",
                                "code": "home"
                            },
                            "source": "ELGATelecomAddressUseFHIRContactPointUse"
                        }
                    ],
                    "HP": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-telecomaddressuse",
                                "code": "home"
                            },
                            "source": "ELGATelecomAddressUseFHIRContactPointUse"
                        }
                    ],
                    "HV": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-telecomaddressuse",
                                "code": "home"
                            },
                            "source": "ELGATelecomAddressUseFHIRContactPointUse"
                        }
                    ],
                    "WP": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-telecomaddressuse",
                                "code": "work"
                            },
                            "source": "ELGATelecomAddressUseFHIRContactPointUse"
                        }
                    ],
                    "AS": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-telecomaddressuse",
                                "code": "work"
                            },
                            "source": "ELGATelecomAddressUseFHIRContactPointUse"
                        }
                    ],
                    "EC": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-telecomaddressuse",
                                "code": "home"
                            },
                            "source": "ELGATelecomAddressUseFHIRContactPointUse"
                        }
                    ],
                    "MC": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-telecomaddressuse",
                                "code": "mobile"
                            },
                            "source": "ELGATelecomAddressUseFHIRContactPointUse"
                        }
                    ],
                    "PG": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-telecomaddressuse",
                                "code": "mobile"
                            },
                            "source": "ELGATelecomAddressUseFHIRContactPointUse"
                        }
                    ],
                    "TMP": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-telecomaddressuse",
                                "code": "temp"
                            },
                            "source": "ELGATelecomAddressUseFHIRContactPointUse"
                        }
                    ]
                }
            }
        }
    }
}

conceptMap_as_7dimension_dict["ELGAEntityNameUseFHIRNameUse"] = {
    "%": {
        "%": {
            "https://termgit.elga.gv.at/ValueSet-elga-entitynameuse": {
                "http://hl7.org/fhir/ValueSet/name-use": {
                    "ASGN": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynameuse",
                                "code": "usual"
                            },
                            "source": "ELGAEntityNameUseFHIRNameUse"
                        }
                    ],
                    "C": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynameuse",
                                "code": "usual"
                            },
                            "source": "ELGAEntityNameUseFHIRNameUse"
                        }
                    ],
                    "I": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynameuse",
                                "code": "anonymous"
                            },
                            "source": "ELGAEntityNameUseFHIRNameUse"
                        }
                    ],
                    "L": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynameuse",
                                "code": "official"
                            },
                            "source": "ELGAEntityNameUseFHIRNameUse"
                        }
                    ],
                    "OR": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynameuse",
                                "code": "official"
                            },
                            "source": "ELGAEntityNameUseFHIRNameUse"
                        }
                    ],
                    "P": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynameuse",
                                "code": "anonymous"
                            },
                            "source": "ELGAEntityNameUseFHIRNameUse"
                        }
                    ],
                    "A": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynameuse",
                                "code": "anonymous"
                            },
                            "source": "ELGAEntityNameUseFHIRNameUse"
                        }
                    ],
                    "R": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynameuse",
                                "code": "anonymous"
                            },
                            "source": "ELGAEntityNameUseFHIRNameUse"
                        }
                    ],
                    "SRCH": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynameuse",
                                "code": "temp"
                            },
                            "source": "ELGAEntityNameUseFHIRNameUse"
                        }
                    ],
                    "PHON": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynameuse",
                                "code": "nickname"
                            },
                            "source": "ELGAEntityNameUseFHIRNameUse"
                        }
                    ],
                    "SNDX": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynameuse",
                                "code": "nickname"
                            },
                            "source": "ELGAEntityNameUseFHIRNameUse"
                        }
                    ],
                    "ABC": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynameuse",
                                "code": "nickname"
                            },
                            "source": "ELGAEntityNameUseFHIRNameUse"
                        }
                    ],
                    "IDE": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynameuse",
                                "code": "nickname"
                            },
                            "source": "ELGAEntityNameUseFHIRNameUse"
                        }
                    ],
                    "SYL": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynameuse",
                                "code": "nickname"
                            },
                            "source": "ELGAEntityNameUseFHIRNameUse"
                        }
                    ]
                }
            }
        }
    }
}

conceptMap_as_7dimension_dict["ELGAEntityNamePartQualifierFHIRNamePartQualifier"] = {
    "%": {
        "%": {
            "https://termgit.elga.gv.at/ValueSet-elga-entitynamepartqualifier": {
                "http://hl7.org/fhir/ValueSet/name-part-qualifier": {
                    "AC": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynamepartqualifier",
                                "code": "AC"
                            },
                            "source": "ELGAEntityNamePartQualifierFHIRNamePartQualifier"
                        }
                    ],
                    "AD": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynamepartqualifier",
                                "code": "AD"
                            },
                            "source": "ELGAEntityNamePartQualifierFHIRNamePartQualifier"
                        }
                    ],
                    "BR": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynamepartqualifier",
                                "code": "BR"
                            },
                            "source": "ELGAEntityNamePartQualifierFHIRNamePartQualifier"
                        }
                    ],
                    "CL": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynamepartqualifier",
                                "code": "CL"
                            },
                            "source": "ELGAEntityNamePartQualifierFHIRNamePartQualifier"
                        }
                    ],
                    "IN": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynamepartqualifier",
                                "code": "IN"
                            },
                            "source": "ELGAEntityNamePartQualifierFHIRNamePartQualifier"
                        }
                    ],
                    "LS": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynamepartqualifier",
                                "code": "LS"
                            },
                            "source": "ELGAEntityNamePartQualifierFHIRNamePartQualifier"
                        }
                    ],
                    "NB": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynamepartqualifier",
                                "code": "NB"
                            },
                            "source": "ELGAEntityNamePartQualifierFHIRNamePartQualifier"
                        }
                    ],
                    "PR": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynamepartqualifier",
                                "code": "PR"
                            },
                            "source": "ELGAEntityNamePartQualifierFHIRNamePartQualifier"
                        }
                    ],
                    "SP": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynamepartqualifier",
                                "code": "SP"
                            },
                            "source": "ELGAEntityNamePartQualifierFHIRNamePartQualifier"
                        }
                    ],
                    "VV": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "https://termgit.elga.gv.at/ValueSet-elga-entitynamepartqualifier",
                                "code": "VV"
                            },
                            "source": "ELGAEntityNamePartQualifierFHIRNamePartQualifier"
                        }
                    ]
                }
            }
        }
    }
}

conceptMap_as_7dimension_dict["OIDtoURI"] = {
    "%": {
        "%": {
            "http://cda.oid": {
                "http://fhir.system": {
                    "2.16.840.1.113883.6.96": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://snomed.info/sct"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.6.1": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://loinc.org"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.6.8": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://unitsofmeasure.org"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.6.3": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://hl7.org/fhir/sid/icd-10"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.6.73": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://www.whocc.no/atc"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.2.16.1.4.9": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "urn:oid:2.16.840.1.113883.2.16.1.4.9"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.83": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "0.4.0.127.0.16.1.1.2.1": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ehdsi-edqm-auszug"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.0.3166.1.2.2": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/iso-3166-alpha-2-code"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.0.3166.1.2.3": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/iso-3166-1-alpha-3"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.0.5218": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/geschlechtercodes-iso-iec-5218"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.0.639.2": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/iso-639-2"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.276.0.76.5.547": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/atc-deutsch-wido"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.10.1.4.3.4.3.2": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-medikationmengenartalternativ"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.10.1.4.3.4.3.3": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/medikationrezeptart"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.10.1.4.3.4.3.4": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/medikationartanwendung"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.10.1.4.3.4.3.5": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/medikationdarreichungsform"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.10.1.4.3.4.3.6": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/medikationtherapieart"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.10.1.4.3.4.3.7": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/medikationrezeptpflichtstatus"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.10": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-languagecode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.11": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-maritalstatus"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.13": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-observationinterpretation"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.14": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/langid-at"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.15": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-participationfunctioncode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.150": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-auditeventid"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.151": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-auditeventtype"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.152": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-auditsourcetype"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.153": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-auditroleid"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.154": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-auditparticipantobjecttype"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.155": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-auditparticipantobjecttyperole"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.156": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-auditparticipantobjectidtype"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.158": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/dicom-sopclasses"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.159": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-medikationabgabeart"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.16": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-addressuse"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.160": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-actcode-abginfo"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.161": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-actcode-patinfo"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.162": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-wirkstoffe-ages"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.164": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-sectionspflegesitber"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.165": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-auditeventtype-a-arr"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.166": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-dosisparameter"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.167": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-problemstatuscode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.168": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-diagnosesicherheit"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.169": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-problemkataloge"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.17": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-personalrelationship"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.171": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-kulturerregernachweis"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.172": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-laendercodes"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.173": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-humanlanguage"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.174": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-proficiencylevelcode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.175": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-languageabilitymode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.176": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-seitenlokalisation"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.177": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-allergyorintolerancetype"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.178": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-absentorunknownallergies"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.179": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-absentorunknownproblems"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.18": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-religiousaffiliation"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.180": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-allergyorintoleranceagent"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.181": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-allergyreaction"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.182": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-criticalityobservationvalue"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.183": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-allergystatuscode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.184": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-conditionverificationstatus"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.186": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-nachweisergebnis"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.187": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-probenmaterial"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.188": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-mikroorganismen"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.189": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-problemseverity"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.19": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-roleclass"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.191": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-absentorunknownmedication"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.192": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-absentorunknowndevices"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.193": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-absentorunknownprocedures"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.198": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-conditionstatuscode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.2": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-nullflavor"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.202": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-expecteddeliverydatemethod"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.203": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-pregnanciessummary"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.204": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-currentsmokingstatus"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.205": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-typeofproblem"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.206": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-allergietyp"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.210": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/atcdabbr-noinformationqualifier"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.211": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/atcdabbr-lateralityqualifiercode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.22": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-serviceeventslabor"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.25": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-urlscheme"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.26": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-rollen"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.27": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-entitynameuse"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.29": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-informationrecipienttype"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.3": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-realmcode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.30": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-medikationtherapieart"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.32": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-medikationmengenart"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.33": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-noinformation"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.34": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-vitalparameterarten"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.35": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-problemarten"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.36": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-telecomaddressuse"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.360": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-sectionsserviceevents"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.39": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-dokumentenklassen"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.4": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-administrativegender"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.42": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-medientyp"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.43": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-serviceeventperformer"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.44": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-laborparameter"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.46": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-specimentype"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.47": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-laborstruktur"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.48": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-sectionsentlassungaerztl"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.49": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-sectionsentlassungpflege"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.5": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-actencountercode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.50": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-sectionsradiologie"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.52": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-humanactsite"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.53": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-entlassungsmanagementa"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.55": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-mammogramassessment"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.57": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-serviceeventsentlassbr"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.58": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-significantpathogens"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.59": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-einnahmezeitpunkte"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.6": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-authorspeciality"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.60": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-formatcodezusatz"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.61": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-formatcode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.62": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/appc-modalitaet"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.63": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/appc-lateralitaet"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.64": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/appc-prozeduren"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.65": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/appc-anatomie"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.66": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-medikationartanwendung"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.67": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-medikationmengenartalternativ"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.68": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-medikationrezeptart"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.69": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-medikationfrequenz"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.7": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-confidentiality"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.70": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-medikationdarreichungsform"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.71": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-medikationpharmazeutischeempfehlungstatus"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.72": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-healthcarefacilitytypecode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.74": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-medikationrezeptpflichtstatus"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.75": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-practicesetting"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.86": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/hl7-at-xds-dokumentenklassen"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.9": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-insuredassocentity"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.90": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ems-anti-hcv-immunoassay"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.91": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ems-anti-hcv-immunoblot-assay"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.92": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ems-hcv-core-ag-assay"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.10.93": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ems-hbv-status"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.3.1.10": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/oeaek-berechtigungen"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.3.1.10.20": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/oeaek-fachrichtung"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.3.1.10.30": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/oeaek-additivfach"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.3.1.10.40": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/oeaek-spezialdiplom"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.3.1.10.50": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/oeaek-zertifikate"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.3.1.10.60": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/oeaek-spezialisierung"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.4.16": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/asp-liste"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.4.16.1": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/eimpf-impfstoffe"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.101": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-parameter"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.102": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-methoden"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.103": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-actcode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.104": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/rast-klassen"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.105": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-krankheitsmerkmale"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.106": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-hcv-rna"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.109": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-klinischemanifestation"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.11": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-laborparameterergaenzung"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.110": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-wurdekrankheitimportiert"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.12": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-practicesetting"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.150": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-auditeventid"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.151": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-auditeventtype"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.152": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-auditsourcetype"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.153": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-auditparticipantobjecttype"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.154": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-auditparticipantobjecttyperole"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.155": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-auditparticipantobjectidtype"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.156": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/medikation-ages-wirkstoffe"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.158": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-funktionsrollen"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.159": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-e-health-anwendungen"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.160": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-fachaerzte"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.161": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-kontakttypen"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.162": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-patienten-identifizierungsmethoden"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.165": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-auditeventtypea-arr"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.171": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/icd-10-bmg-2017"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.173": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-specimentype-ergaenzung"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.175": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/icpc2"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.179": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-ergaenzungsliste"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.180": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-allergietyp"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.183": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/eimpf-ergaenzung"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.184": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/icd-10-bmg-2020"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.186": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/eimpf-historischeimpfstoffe"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.187": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-ergaenzungmeldepflichtigekrankheiten"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.190": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-pflegestufen"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.191": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/eimpf-zuordnungsmatrix"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.194": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/exnds-sections"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.195": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/exnds-concepts"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.196": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-betreuung"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.197": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-listeschulen"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.198": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/exnds-metadaten"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.199": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/exnds-formatcodes"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.2": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-gtelvogdarollen"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.200": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/eimpf-schemamatrix"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.202": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/dgc-qr"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.203": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/dgc-antibody-test"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.205": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/dgc-ratnamemanufacturer"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.206": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/lkf-diagnose-typ"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.207": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/lkf-diagnose-art"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.208": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/lkf-diagnose-statauf"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.209": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/bmg-icd-10-2022"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.21": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-serviceeventsentlassbrief"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.211": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/lkf-ergaenzung"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.215": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-lebensmittelallergene"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.216": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/bmg-lkf-2023"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.217": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/austrian-designation-use"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.219": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/medikationpackaging"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.221": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/medikationactiveingredient"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.222": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/bmg-icd-10-2024"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.223": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/bmg-lkf-2024"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.224": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/hl7-at-administrativegender-ergaenzung"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.28": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-entlassungsmanagementart"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.3": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-gda-aggregatrollen"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.37": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-formatcode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.38.1": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/appc-modalitaet"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.38.2": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/appc-lateralitaet"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.38.3": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/appc-prozeduren"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.38.4": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/appc-anatomie"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.4": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/gda-attribute"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.40": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-sections"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.41": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-formatcodezusatz"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.45": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-significantpathogens"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.49": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-mammogramassessment"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.5": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/gda-org"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.55": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/elga-urlschemeergaenzung"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.56": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/icd-10-bmg-2014"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.58": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-material"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.59": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-janein"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.60": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-analysedetails"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.61": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-antigenh"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.62": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-artmalaria"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.63": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-artquartier"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.64": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-befundart"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.65": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-biotyp-biovar"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.66": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-antigeno"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.67": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-tbc-resistenzergaenzung"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.68": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-quartiercode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.69": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-aviditaet"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.70": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-genogruppe"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.71": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-genotyp"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.72": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-genotyppora-r1"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.73": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-genotyppora-r2"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.74": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-durchgefuehrt"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.75": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-tbc-resultat"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.76": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-ergebnis"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.77": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-wowurdekrankheiterworben"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.78": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-nachweisbar"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.79": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-testmethodemic-ipd"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.80": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-testmethodetypingipd"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.81": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-nachweis"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.82": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-multilocsequ"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.83": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-monoclonalsub"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.84": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-organ"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.85": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-yersinapathogen"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.86": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-phagentyp-vtec"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.87": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-phagentyp"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.88": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-posneg"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.89": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-ribotype"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.90": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-serogruppe"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.91": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-serotyp-gene-feta"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.92": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-serotyp"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.93": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-gewinnung"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.94": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-tbc-typ"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.95": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-orth20probe"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.96": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-reiseland"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.97": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-verotoxin-2-subtyp"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.98": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-verotoxin-1-subtyp"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.5.99": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ems-materialmethode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.10": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/eimpf-historischeimpfstoffe"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.11": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/eimpf-impfrollen"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.13": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/eimpf-antikoerperbestimmung"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.14": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/eimpf-impfstoffe"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.15": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/eimpf-specialsituationindication"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.16": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ems-materialmethode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.18": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ems-krankheitsmerkmale"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.19": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ems-meldepflichtige-krankheiten"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.2": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/eimpf-impfrelevanteerkrankung"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.21": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ems-taetigkeitsbereich"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.23": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-artderdiagnose"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.24": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ems-impfstatus"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.25": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ems-klinischemanifestation"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.26": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-serviceeventstelemonepi"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.27": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/hl7-at-actconsenttype"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.29": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ems-lebensmittelbedingteintoxikationen"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.3": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/eimpf-specialcasevaccination"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.30": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-alcoholconsumption"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.31": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ems-betreuung"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.4": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/eimpf-immunizationtarget"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.49": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ems-hospitalisierung"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.5": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/eimpf-impfschema"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.51": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ems-reiseland"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.52": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-pregnancystatus"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.53": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-antibiogramm"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.54": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/dgc-typeoftest"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.55": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/dgc-diseaseoragent"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.56": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/dgc-vaccine"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.57": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/dgc-medicinalproduct"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.58": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/dgc-vaccinemarketingauthorizationholder"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.59": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/dgc-doses"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.6": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/eimpf-impfdosis"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.60": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/dgc-resultofthetest"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.62": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/eimpf-zusatzklassifikation"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.63": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/dgc-country"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.65": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/dgc-ratnamemanufacturer"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.66": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-anamneselabormikrobiologie"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.67": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/lkf-diagnose-art"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.68": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/lkf-diagnose-statauf"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.69": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/lkf-diagnose-typ"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.7": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/eimpf-impfgrund"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.74": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/eimpf-mengenart"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.75": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-lebensmittelallergene"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.76": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/austrian-designation-use"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.77": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/hl7-at-patientidentifier"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.78": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/eimpf-zusatzklassifikation-impfprogramm"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.79": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/eimpf-zusatzklassifikation-impfsetting"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.8": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/elga-entitynamepartqualifier"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.81": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/hl7-at-administrativegender-v2"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.83": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/hl7-at-administrativegender-fhir-extension"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.84": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/orphanet-rare-diseases"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.85": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/snomed-rare-diseases"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.86": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/hl7-at-organizationtype"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.40.0.34.6.0.10.87": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/hl7-at-practitionerrole"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.840.10003.5.109": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/iana-mime-type"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.840.10008.2.16.4": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/dcm"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.2.840.10008.2.6.1": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/dicom-sopclasses"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.3.6.1.4.1.12559.11.10.1.3.1.42.1": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ehdsi-healthcare-professional-role"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.3.6.1.4.1.12559.11.10.1.3.1.42.12": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ehdsi-route-of-administration"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.3.6.1.4.1.12559.11.10.1.3.1.42.16": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ehdsi-unit"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.3.6.1.4.1.12559.11.10.1.3.1.42.2": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ehdsi-doseform"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.3.6.1.4.1.12559.11.10.1.3.1.42.24": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ehdsi-activeingredient"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.3.6.1.4.1.12559.11.10.1.3.1.42.3": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ehdsi-package"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.3.6.1.4.1.12559.11.10.1.3.1.42.31": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ehdsi-confidentiality"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.3.6.1.4.1.12559.11.10.1.3.1.42.34": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ehdsi-administrative-gender"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.3.6.1.4.1.12559.11.10.1.3.1.42.4": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ehdsi-country"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.3.6.1.4.1.12559.11.10.1.3.1.42.40": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ehdsi-telecom-address"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.3.6.1.4.1.12559.11.10.1.3.1.42.41": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ehdsi-timing-event"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.3.6.1.4.1.12559.11.10.1.3.1.42.56": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ehdsi-quantity-unit"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.3.6.1.4.1.12559.11.10.1.3.1.42.6": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ehdsi-language"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.3.6.1.4.1.12559.11.10.1.3.1.42.61": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ehdsi-substance"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1.3.6.1.4.1.19376.1.9.2.1": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ihe-pharmaceutical-advice-status-list"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "1dd183a6-6d2b-4a9d-8f5d-be09d6bb5a6e": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ehdsi-language"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.1.11.19708": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/ValueSet/ehdsi-actsubstanceadministrationcode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.12.1": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/hl7-administrative-sex"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.12.496": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/hl7-consent-type"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.12.497": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/hl7-consent-mode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.12.498": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/hl7-consent-status"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.12.548": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/hl7-signatorys-relationship-to-subject"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.18.108": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v2-0203"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.18.2": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v2-0001"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.18.320": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v2-0496"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.18.321": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v2-0497"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.18.322": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v2-0498"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.18.355": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v2-0548"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.2.16.1.4.1": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://hl7.at/fhir/HL7ATCoreProfiles/4.0.1/CodeSystem/at-core-cs-religion"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.2.16.1.4.10": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/hl7-at-formatcodes"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.2.9.6.2.7": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/isco"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.3.6905.2": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ehdsi-substance"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.3.7.1.7": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/sciphox-seitenlokalisation"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.3.7.1.8": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/sciphox-diagnosenzusatz"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.4.642.1.76": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://hl7.org/fhir/event-timing"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.4.642.3.115": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ips-conditionverificationstatus"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.4.642.3.155": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ips-conditionclinicalstatuscodes"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.1": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v3-AdministrativeGender"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.1008": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v3-NullFlavor"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.1052": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v3-ActSite"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.110": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v3-RoleClass"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.111": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v3-RoleCode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.1119": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v3-AddressUse"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.1150.1": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/ips-absentorunknowndata"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.129": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v3-SpecimenType"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.139": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v3-TimingEvent"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.14": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v3-ActStatus"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.143": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v3-URLScheme"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.2": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v3-MaritalStatus"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.25": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v3-Confidentiality"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.4": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v3-ActCode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.43": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v3-EntityNamePartQualifier"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.45": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v3-EntityNameUse"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.60": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v3-LanguageAbilityMode"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.61": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v3-LanguageAbilityProficiency"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.88": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v3-ParticipationFunction"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.5.90": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.6.121": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/hl7-language-identification"
                            },
                            "source": "OIDtoURI"
                        },
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "urn:ietf:bcp:47"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.6.24": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/mdc-medicaldevicecommunications"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.6.254-2005": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/icf"
                            },
                            "source": "OIDtoURI"
                        }
                    ],
                    "2.16.840.1.113883.6.43.1": [
                        {
                            "relationship": "equivalent",
                            "concept": {
                                "system": "http://cda.oid",
                                "code": "https://termgit.elga.gv.at/CodeSystem/icd-o-3"
                            },
                            "source": "OIDtoURI"
                        }
                    ]
                }
            }
        }
    }
}
def II(src, tgt):
    Any(src, tgt)
    r = src.root
    if r:
        if fhirpath.single([bool([v2 for v1 in [src] for v2 in fhirpath_utils.get(v1,'extension')])]):
            tgt.system = string(value=translate_single('OIDtoURI', (r if isinstance(r, str) else r.value), 'code'))
    r = src.root
    if r:
        if fhirpath.single(fhirpath_utils.bool_and([not([v2 for v1 in [src] for v2 in fhirpath_utils.get(v1,'extension')])], [v6 for v5 in [v4 for v3 in [src] for v4 in fhirpath_utils.get(v3,'root')] for v6 in fhirpath_utils.matches(v5, ['[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'])])):
            tgt.system = uri(value='urn:ietf:rfc:3986')
            tgt.value = string(value=fhirpath.single(fhirpath_utils.add(['urn:uuid:'], [v2 for v1 in [r] for v2 in fhirpath_utils.lower(v1)])))
    r = src.root
    if r:
        if fhirpath.single(fhirpath_utils.bool_and([not([v2 for v1 in [src] for v2 in fhirpath_utils.get(v1,'extension')])], [v6 for v5 in [v4 for v3 in [src] for v4 in fhirpath_utils.get(v3,'root')] for v6 in fhirpath_utils.contains(v5, ['.'])])):
            tgt.system = uri(value='urn:ietf:rfc:3986')
            tgt.value = string(value=('urn:oid:' + ('' if r is None else r if isinstance(r, str) else r.value)))
    e = src.extension
    if e:
        tgt.value = string(value=e)
    s = src.assigningAuthorityName
    if s:
        a = malac.models.fhir.r4.Reference()
        if tgt.assigner is not None:
            a = tgt.assigner
        else:
            tgt.assigner = a
        a.display = string(value=s)
    displayable = src.displayable
    if displayable:
        ext = malac.models.fhir.r4.Extension()
        tgt.extension.append(ext)
        ext.url = 'http://hl7.org/cda/stds/core/StructureDefinition/extension-displayable'
        v = displayable.value
        if v:
            ext.valueString = string(value=str(v))

def INT(src, tgt):
    Any(src, tgt)
    v = src.value
    if v:
        tgt.value = v

def BL(src, tgt):
    Any(src, tgt)
    v = src.value
    if v:
        tgt.value = v

def TSInstant(src, tgt):
    Any(src, tgt)
    v = src.value
    if v:
        tgt.value = dateutil.parser.parse(str(v))

def IVL_TSDateTime(src, tgt):
    TSInstant(src, tgt)

def TSDateTime(src, tgt):
    TSInstant(src, tgt)

def IVXB_TSDateTime(src, tgt):
    TSDateTime(src, tgt)

def TSDate(src, tgt):
    TSInstant(src, tgt)
    v = src.value
    if v:
        tgt.value = ('' if v is None else v if isinstance(v, str) else v.value)[:10]

def IVLTSPeriod(src, tgt):
    Any(src, tgt)
    if src.low:
        tgt.start = malac.models.fhir.r4.dateTime()
        transform_default(src.low, tgt.start)
    if src.high:
        tgt.end = malac.models.fhir.r4.dateTime()
        transform_default(src.high, tgt.end)

def IVLTSDateTime(src, tgt):
    Any(src, tgt)
    s = src.low
    if s:
        TSDateTime(s, tgt)

def STstring(src, tgt):
    Any(src, tgt)
    v = src
    if v:
        tgt.value = fhirpath.single([v2 for v1 in [v] for v2 in fhirpath_utils.get(v1,'valueOf_',strip=True)])

def EDstring(src, tgt):
    STstring(src, tgt)

def ENstring(src, tgt):
    Any(src, tgt)
    v = src
    if v:
        tgt.value = fhirpath.single([v2 for v1 in [v] for v2 in fhirpath_utils.get(v1,'valueOf_',strip=True)])

def ONstring(src, tgt):
    ENstring(src, tgt)

def CSCode(src, tgt):
    Any(src, tgt)
    c = src.code
    if c:
        tgt.value = c

def CECode(src, tgt):
    CSCode(src, tgt)

def CDCode(src, tgt):
    CSCode(src, tgt)

def CECoding(src, tgt):
    Any(src, tgt)
    code = src.code
    if code:
        tgt.code = string(value=str(code))
    system = src.codeSystem
    if system:
        tgt.system = string(value=translate_single('OIDtoURI', (system if isinstance(system, str) else system.value), 'code'))

def CDCoding(src, tgt):
    CECoding(src, tgt)

def CECodeableConcept(src, tgt):
    Any(src, tgt)
    if src.originalText:
        tgt.text = malac.models.fhir.r4.string()
        EDstring(src.originalText, tgt.text)
    coding = malac.models.fhir.r4.Coding()
    tgt.coding.append(coding)
    CECoding(src, coding)
    for translation in src.translation or []:
        coding = malac.models.fhir.r4.Coding()
        tgt.coding.append(coding)
        code = translation.code
        if code:
            coding.code = string(value=str(code))
        system = src.codeSystem
        if system:
            tgt.systemCode = string(value=translate_single('OIDtoURI', (system if isinstance(system, str) else system.value), 'code'))

def CSCodeableConcept(src, tgt):
    CECodeableConcept(src, tgt)

def CDCodeableConcept(src, tgt):
    CECodeableConcept(src, tgt)

def CdaPersonNameCompilationToFhirHumanName(cda_name, fhir_humanName):
    Any(cda_name, fhir_humanName)
    cda_name_use = cda_name.use
    if cda_name_use:
        fhir_humanName.use = string(value=translate_single('ELGAEntityNameUseFHIRNameUse', (cda_name_use if isinstance(cda_name_use, str) else cda_name_use.value), 'code'))
    cda_name_text = cda_name.valueOf_.strip()
    if cda_name_text:
        fhir_humanName.text = string(value=fhirpath.single([cda_name_text]))
    for cda_name_prefix in cda_name.prefix or []:
        fhir_humanName_prefix = [string(value=v3) for v3 in [v2 for v1 in [cda_name_prefix] for v2 in fhirpath_utils.get(v1,'valueOf_',strip=True)]]
        for v4 in fhir_humanName_prefix:
            fhir_humanName.prefix.append(v4)
        extension = []
        for _fhir_humanName_prefix in fhir_humanName_prefix:
            _extension = malac.models.fhir.r4.Extension()
            _fhir_humanName_prefix.extension.append(_extension)
            extension.append(_extension)
        if fhirpath.single([bool([v2 for v1 in [cda_name_prefix] for v2 in fhirpath_utils.get(v1,'qualifier')])]):
            for _extension in extension:
                _extension.url = 'http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier'
        qualifier = cda_name_prefix.qualifier
        if qualifier:
            for _extension in extension:
                _extension.valueCode = string(value=translate_single('ELGAEntityNamePartQualifierFHIRNamePartQualifier', (qualifier if isinstance(qualifier, str) else qualifier.value), 'code'))
    for cda_name_given in cda_name.given or []:
        fhir_humanName_given = [string(value=v3) for v3 in [v2 for v1 in [cda_name_given] for v2 in fhirpath_utils.get(v1,'valueOf_',strip=True)]]
        for v4 in fhir_humanName_given:
            fhir_humanName.given.append(v4)
        extension = []
        for _fhir_humanName_given in fhir_humanName_given:
            _extension = malac.models.fhir.r4.Extension()
            _fhir_humanName_given.extension.append(_extension)
            extension.append(_extension)
        if fhirpath.single([bool([v2 for v1 in [cda_name_given] for v2 in fhirpath_utils.get(v1,'qualifier')])]):
            for _extension in extension:
                _extension.url = 'http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier'
        qualifier = cda_name_given.qualifier
        if qualifier:
            for _extension in extension:
                _extension.valueCode = string(value=translate_single('ELGAEntityNamePartQualifierFHIRNamePartQualifier', (qualifier if isinstance(qualifier, str) else qualifier.value), 'code'))
    for cda_name_family in cda_name.family or []:
        fhir_humanName_family = string(value=fhirpath.single([v2 for v1 in [cda_name_family] for v2 in fhirpath_utils.get(v1,'valueOf_',strip=True)]))
        fhir_humanName.family = fhir_humanName_family
        if fhir_humanName_family:
            extension = malac.models.fhir.r4.Extension()
            fhir_humanName_family.extension.append(extension)
        else:
            extension = None
        if fhirpath.single([bool([v2 for v1 in [cda_name_family] for v2 in fhirpath_utils.get(v1,'qualifier')])]):
            if extension:
                extension.url = 'http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier'
        qualifier = cda_name_family.qualifier
        if qualifier:
            if extension:
                extension.valueCode = string(value=translate_single('ELGAEntityNamePartQualifierFHIRNamePartQualifier', (qualifier if isinstance(qualifier, str) else qualifier.value), 'code'))
    for cda_name_suffix in cda_name.suffix or []:
        fhir_humanName_suffix = [string(value=v3) for v3 in [v2 for v1 in [cda_name_suffix] for v2 in fhirpath_utils.get(v1,'valueOf_',strip=True)]]
        for v4 in fhir_humanName_suffix:
            fhir_humanName.suffix.append(v4)
        extension = []
        for _fhir_humanName_suffix in fhir_humanName_suffix:
            _extension = malac.models.fhir.r4.Extension()
            _fhir_humanName_suffix.extension.append(_extension)
            extension.append(_extension)
        if fhirpath.single([bool([v2 for v1 in [cda_name_suffix] for v2 in fhirpath_utils.get(v1,'qualifier')])]):
            for _extension in extension:
                _extension.url = 'http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier'
        qualifier = cda_name_suffix.qualifier
        if qualifier:
            for _extension in extension:
                _extension.valueCode = string(value=translate_single('ELGAEntityNamePartQualifierFHIRNamePartQualifier', (qualifier if isinstance(qualifier, str) else qualifier.value), 'code'))

def CdaOrganizationCompilationToFhirOrganization(cda_organization, fhir_organization):
    for id_ in cda_organization.id or []:
        fhir_organization.identifier.append(malac.models.fhir.r4.Identifier())
        II(id_, fhir_organization.identifier[-1])
    for name in cda_organization.name or []:
        fhir_organization.name = malac.models.fhir.r4.string()
        transform_default(name, fhir_organization.name)
    for telecom in cda_organization.telecom or []:
        fhir_organization.telecom.append(malac.models.fhir.r4.ContactPoint())
        TELContactPoint(telecom, fhir_organization.telecom[-1])
    for addr in cda_organization.addr or []:
        fhir_organization.address.append(malac.models.fhir.r4.Address())
        CdaAdressCompilationToFhirAustrianAddress(addr, fhir_organization.address[-1])

def CdaAdressCompilationToFhirAustrianAddress(cda_address, fhir_address):
    Any(cda_address, fhir_address)
    cda_use = cda_address.use
    if cda_use:
        fhir_address.use = string(value=translate_single('ELGA2FHIRAddressUse', (cda_use if isinstance(cda_use, str) else cda_use.value), 'code'))
        if fhirpath.single(fhirpath_utils.bool_and(fhirpath_utils.equals([cda_use], '!=', ['PHYS']), fhirpath_utils.equals([cda_use], '!=', ['PST']))):
            fhir_address.type_ = string(value='both')
        if fhirpath.single(fhirpath_utils.equals([cda_use], '==', ['PHYS'])):
            fhir_address.type_ = string(value='physical')
        if fhirpath.single(fhirpath_utils.equals([cda_use], '==', ['PST'])):
            fhir_address.type_ = string(value='postal')
    for cda_postalCode in cda_address.postalCode or []:
        fhir_address.postalCode = string(value=fhirpath.single([v2 for v1 in [cda_postalCode] for v2 in fhirpath_utils.get(v1,'valueOf_',strip=True)]))
    for cda_city in cda_address.city or []:
        fhir_address.city = string(value=fhirpath.single([v2 for v1 in [cda_city] for v2 in fhirpath_utils.get(v1,'valueOf_',strip=True)]))
    for cda_state in cda_address.state or []:
        fhir_address.state = string(value=fhirpath.single([v2 for v1 in [cda_state] for v2 in fhirpath_utils.get(v1,'valueOf_',strip=True)]))
    for cda_country in cda_address.country or []:
        fhir_address.country = string(value=fhirpath.single([v2 for v1 in [cda_country] for v2 in fhirpath_utils.get(v1,'valueOf_',strip=True)]))
    if fhirpath.single(fhirpath_utils.bool_and([bool([v2 for v1 in [cda_address] for v2 in fhirpath_utils.get(v1,'streetName')])], [bool([v5 for v4 in [cda_address] for v5 in fhirpath_utils.get(v4,'houseNumber')])])):
        fhir_address_line = malac.models.fhir.r4.string()
        fhir_address.line.append(fhir_address_line)
        if fhirpath.single([bool([v2 for v1 in [cda_address] for v2 in fhirpath_utils.get(v1,'additionalLocator')])]):
            fhir_address_line.value = fhirpath.single(fhirpath_utils.add(fhirpath_utils.add(fhirpath_utils.add(fhirpath_utils.add([v4 for v3 in [v2 for v1 in [cda_address] for v2 in fhirpath_utils.get(v1,'streetName')] for v4 in fhirpath_utils.get(v3,'valueOf_',strip=True)], [' ']), [v8 for v7 in [v6 for v5 in [cda_address] for v6 in fhirpath_utils.get(v5,'houseNumber')] for v8 in fhirpath_utils.get(v7,'valueOf_',strip=True)]), [' ']), [v12 for v11 in [v10 for v9 in [cda_address] for v10 in fhirpath_utils.get(v9,'additionalLocator')] for v12 in fhirpath_utils.get(v11,'valueOf_',strip=True)]))
        if fhirpath.single(fhirpath_utils.bool_not([bool([v2 for v1 in [cda_address] for v2 in fhirpath_utils.get(v1,'additionalLocator')])])):
            fhir_address_line.value = fhirpath.single(fhirpath_utils.add(fhirpath_utils.add([v4 for v3 in [v2 for v1 in [cda_address] for v2 in fhirpath_utils.get(v1,'streetName')] for v4 in fhirpath_utils.get(v3,'valueOf_',strip=True)], [' ']), [v8 for v7 in [v6 for v5 in [cda_address] for v6 in fhirpath_utils.get(v5,'houseNumber')] for v8 in fhirpath_utils.get(v7,'valueOf_',strip=True)]))
        for cda_address_streetName in cda_address.streetName or []:
            extension = malac.models.fhir.r4.Extension()
            fhir_address_line.extension.append(extension)
            extension.url = 'http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-streetName'
            extension.valueString = string(value=fhirpath.single([v2 for v1 in [cda_address_streetName] for v2 in fhirpath_utils.get(v1,'valueOf_',strip=True)]))
        for cda_address_houseNumber in cda_address.houseNumber or []:
            extension = malac.models.fhir.r4.Extension()
            fhir_address_line.extension.append(extension)
            extension.url = 'http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-houseNumber'
            extension.valueString = string(value=fhirpath.single([v2 for v1 in [cda_address_houseNumber] for v2 in fhirpath_utils.get(v1,'valueOf_',strip=True)]))
        for cda_address_additionalLocator in cda_address.additionalLocator or []:
            if fhirpath.single([bool([v2 for v1 in [cda_address] for v2 in fhirpath_utils.get(v1,'additionalLocator')])]):
                extension = malac.models.fhir.r4.Extension()
                fhir_address_line.extension.append(extension)
                extension.url = 'http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-additionalLocator'
                extension.valueString = string(value=fhirpath.single([v2 for v1 in [cda_address_additionalLocator] for v2 in fhirpath_utils.get(v1,'valueOf_',strip=True)]))
    if fhirpath.single([bool([v2 for v1 in [cda_address] for v2 in fhirpath_utils.get(v1,'streetAddressLine')])]):
        fhir_address_line = malac.models.fhir.r4.string()
        fhir_address.line.append(fhir_address_line)
        if fhirpath.single([bool([v2 for v1 in [cda_address] for v2 in fhirpath_utils.get(v1,'additionalLocator')])]):
            fhir_address_line.value = fhirpath.single(fhirpath_utils.add(fhirpath_utils.add([v4 for v3 in [v2 for v1 in [cda_address] for v2 in fhirpath_utils.get(v1,'streetAddressLine')] for v4 in fhirpath_utils.get(v3,'valueOf_',strip=True)], [' ']), [v8 for v7 in [v6 for v5 in [cda_address] for v6 in fhirpath_utils.get(v5,'additionalLocator')] for v8 in fhirpath_utils.get(v7,'valueOf_',strip=True)]))
        if fhirpath.single(fhirpath_utils.bool_not([bool([v2 for v1 in [cda_address] for v2 in fhirpath_utils.get(v1,'additionalLocator')])])):
            fhir_address_line.value = fhirpath.single([v4 for v3 in [v2 for v1 in [cda_address] for v2 in fhirpath_utils.get(v1,'streetAddressLine')] for v4 in fhirpath_utils.get(v3,'valueOf_',strip=True)])
        for cda_address_additionalLocator in cda_address.additionalLocator or []:
            if fhirpath.single([bool([v2 for v1 in [cda_address] for v2 in fhirpath_utils.get(v1,'additionalLocator')])]):
                extension = malac.models.fhir.r4.Extension()
                fhir_address_line.extension.append(extension)
                extension.url = 'http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-additionalLocator'
                extension.valueString = string(value=fhirpath.single([v2 for v1 in [cda_address_additionalLocator] for v2 in fhirpath_utils.get(v1,'valueOf_',strip=True)]))

def TELContactPoint(src, tgt):
    Any(src, tgt)
    u = src.use
    if u:
        if fhirpath.single(fhirpath_utils.bool_or([v4 for v3 in [v2 for v1 in [src] for v2 in fhirpath_utils.get(v1,'use')] for v4 in fhirpath_utils.startswith(v3, ['H'])], (fhirpath_utils.equals([v6 for v5 in [src] for v6 in fhirpath_utils.get(v5,'use')], '==', ['EC'])))):
            tgt.use = string(value=translate_single('ELGATelecomAddressUseFHIRContactPointUse', (u if isinstance(u, str) else u.value), 'code'))
    u = src.use
    if u:
        if fhirpath.single(fhirpath_utils.bool_or((fhirpath_utils.equals([v2 for v1 in [src] for v2 in fhirpath_utils.get(v1,'use')], '==', ['WP'])), (fhirpath_utils.equals([v4 for v3 in [src] for v4 in fhirpath_utils.get(v3,'use')], '==', ['AS'])))):
            tgt.use = string(value=translate_single('ELGATelecomAddressUseFHIRContactPointUse', (u if isinstance(u, str) else u.value), 'code'))
    u = src.use
    if u:
        if fhirpath.single(fhirpath_utils.bool_or((fhirpath_utils.equals([v2 for v1 in [src] for v2 in fhirpath_utils.get(v1,'use')], '==', ['MC'])), (fhirpath_utils.equals([v4 for v3 in [src] for v4 in fhirpath_utils.get(v3,'use')], '==', ['PG'])))):
            tgt.use = string(value=translate_single('ELGATelecomAddressUseFHIRContactPointUse', (u if isinstance(u, str) else u.value), 'code'))
    u = src.use
    if u:
        if fhirpath.single((fhirpath_utils.equals([v2 for v1 in [src] for v2 in fhirpath_utils.get(v1,'use')], '==', ['TMP']))):
            tgt.use = string(value=translate_single('ELGATelecomAddressUseFHIRContactPointUse', (u if isinstance(u, str) else u.value), 'code'))
    v = src.value
    if v:
        if fhirpath.single([v4 for v3 in [v2 for v1 in [src] for v2 in fhirpath_utils.get(v1,'value')] for v4 in fhirpath_utils.startswith(v3, ['fax:'])]):
            tgt.value = string(value=fhirpath.single([v2 for v1 in [v] for v2 in fhirpath_utils.substring(v1,[4],[])]))
            tgt.system = string(value='fax')
    v = src.value
    if v:
        if fhirpath.single([v4 for v3 in [v2 for v1 in [src] for v2 in fhirpath_utils.get(v1,'value')] for v4 in fhirpath_utils.startswith(v3, ['file:'])]):
            tgt.value = string(value=fhirpath.single([v2 for v1 in [v] for v2 in fhirpath_utils.substring(v1,[5],[])]))
            tgt.system = string(value='other')
    v = src.value
    if v:
        if fhirpath.single([v4 for v3 in [v2 for v1 in [src] for v2 in fhirpath_utils.get(v1,'value')] for v4 in fhirpath_utils.startswith(v3, ['ftp:'])]):
            tgt.value = string(value=fhirpath.single([v2 for v1 in [v] for v2 in fhirpath_utils.substring(v1,[4],[])]))
            tgt.system = string(value='url')
    v = src.value
    if v:
        if fhirpath.single([v4 for v3 in [v2 for v1 in [src] for v2 in fhirpath_utils.get(v1,'value')] for v4 in fhirpath_utils.startswith(v3, ['http:'])]):
            tgt.value = string(value=fhirpath.single([v2 for v1 in [v] for v2 in fhirpath_utils.substring(v1,[7],[])]))
            tgt.system = string(value='url')
    v = src.value
    if v:
        if fhirpath.single([v4 for v3 in [v2 for v1 in [src] for v2 in fhirpath_utils.get(v1,'value')] for v4 in fhirpath_utils.startswith(v3, ['mailto:'])]):
            tgt.value = string(value=fhirpath.single([v2 for v1 in [v] for v2 in fhirpath_utils.substring(v1,[7],[])]))
            tgt.system = string(value='email')
    v = src.value
    if v:
        if fhirpath.single([v4 for v3 in [v2 for v1 in [src] for v2 in fhirpath_utils.get(v1,'value')] for v4 in fhirpath_utils.startswith(v3, ['mllp:'])]):
            tgt.value = string(value=fhirpath.single([v2 for v1 in [v] for v2 in fhirpath_utils.substring(v1,[5],[])]))
            tgt.system = string(value='url')
    v = src.value
    if v:
        if fhirpath.single([v4 for v3 in [v2 for v1 in [src] for v2 in fhirpath_utils.get(v1,'value')] for v4 in fhirpath_utils.startswith(v3, ['modem:'])]):
            tgt.value = string(value=fhirpath.single([v2 for v1 in [v] for v2 in fhirpath_utils.substring(v1,[6],[])]))
            tgt.system = string(value='other')
    v = src.value
    if v:
        if fhirpath.single([v4 for v3 in [v2 for v1 in [src] for v2 in fhirpath_utils.get(v1,'value')] for v4 in fhirpath_utils.startswith(v3, ['nfs:'])]):
            tgt.value = string(value=fhirpath.single([v2 for v1 in [v] for v2 in fhirpath_utils.substring(v1,[4],[])]))
            tgt.system = string(value='other')
    v = src.value
    if v:
        if fhirpath.single([v4 for v3 in [v2 for v1 in [src] for v2 in fhirpath_utils.get(v1,'value')] for v4 in fhirpath_utils.startswith(v3, ['tel:'])]):
            tgt.value = string(value=fhirpath.single([v2 for v1 in [v] for v2 in fhirpath_utils.substring(v1,[4],[])]))
            tgt.system = string(value='phone')
    v = src.value
    if v:
        if fhirpath.single([v4 for v3 in [v2 for v1 in [src] for v2 in fhirpath_utils.get(v1,'value')] for v4 in fhirpath_utils.startswith(v3, ['telnet:'])]):
            tgt.value = string(value=fhirpath.single([v2 for v1 in [v] for v2 in fhirpath_utils.substring(v1,[7],[])]))
            tgt.system = string(value='url')
    for useablePeriod in src.useablePeriod or []:
        tgt.period = malac.models.fhir.r4.Period()
        transform_default(useablePeriod, tgt.period)

def PQQuantity(src, tgt):
    Any(src, tgt)
    tgt.system = uri(value='http://unitsofmeasure.org')
    unit = src.unit
    if unit:
        tgt.code = string(value=unit)
    value = src.value
    if value:
        tgt.value = malac.models.fhir.r4.decimal(value=value)

def IVLPQRange(src, tgt):
    Any(src, tgt)
    source_low = src.low
    if source_low:
        target_low = malac.models.fhir.r4.Quantity()
        if tgt.low is not None:
            target_low = tgt.low
        else:
            tgt.low = target_low
        PQQuantity(source_low, target_low)
    source_high = src.high
    if source_high:
        target_high = malac.models.fhir.r4.Quantity()
        if tgt.high is not None:
            target_high = tgt.high
        else:
            tgt.high = target_high
        PQQuantity(source_high, target_high)

def IVXB_PQQuantity(src, tgt):
    PQQuantity(src, tgt)

def RTOPQPQRatio(src, tgt):
    Any(src, tgt)
    numerator = src.numerator
    if numerator:
        targetNumerator = malac.models.fhir.r4.Quantity()
        if tgt.numerator is not None:
            targetNumerator = tgt.numerator
        else:
            tgt.numerator = targetNumerator
        PQQuantity(numerator, targetNumerator)
    denominator = src.denominator
    if denominator:
        targetDenominator = malac.models.fhir.r4.Quantity()
        if tgt.denominator is not None:
            targetDenominator = tgt.denominator
        else:
            tgt.denominator = targetDenominator
        PQQuantity(denominator, targetDenominator)

def Any(src, tgt):
    pass

def unpack_container(resource_container):
    if resource_container.Account is not None:
        return resource_container.Account
    if resource_container.ActivityDefinition is not None:
        return resource_container.ActivityDefinition
    if resource_container.AdministrableProductDefinition is not None:
        return resource_container.AdministrableProductDefinition
    if resource_container.AdverseEvent is not None:
        return resource_container.AdverseEvent
    if resource_container.AllergyIntolerance is not None:
        return resource_container.AllergyIntolerance
    if resource_container.Appointment is not None:
        return resource_container.Appointment
    if resource_container.AppointmentResponse is not None:
        return resource_container.AppointmentResponse
    if resource_container.AuditEvent is not None:
        return resource_container.AuditEvent
    if resource_container.Basic is not None:
        return resource_container.Basic
    if resource_container.Binary is not None:
        return resource_container.Binary
    if resource_container.BiologicallyDerivedProduct is not None:
        return resource_container.BiologicallyDerivedProduct
    if resource_container.BodyStructure is not None:
        return resource_container.BodyStructure
    if resource_container.Bundle is not None:
        return resource_container.Bundle
    if resource_container.CapabilityStatement is not None:
        return resource_container.CapabilityStatement
    if resource_container.CarePlan is not None:
        return resource_container.CarePlan
    if resource_container.CareTeam is not None:
        return resource_container.CareTeam
    if resource_container.CatalogEntry is not None:
        return resource_container.CatalogEntry
    if resource_container.ChargeItem is not None:
        return resource_container.ChargeItem
    if resource_container.ChargeItemDefinition is not None:
        return resource_container.ChargeItemDefinition
    if resource_container.Citation is not None:
        return resource_container.Citation
    if resource_container.Claim is not None:
        return resource_container.Claim
    if resource_container.ClaimResponse is not None:
        return resource_container.ClaimResponse
    if resource_container.ClinicalImpression is not None:
        return resource_container.ClinicalImpression
    if resource_container.ClinicalUseDefinition is not None:
        return resource_container.ClinicalUseDefinition
    if resource_container.CodeSystem is not None:
        return resource_container.CodeSystem
    if resource_container.Communication is not None:
        return resource_container.Communication
    if resource_container.CommunicationRequest is not None:
        return resource_container.CommunicationRequest
    if resource_container.CompartmentDefinition is not None:
        return resource_container.CompartmentDefinition
    if resource_container.Composition is not None:
        return resource_container.Composition
    if resource_container.ConceptMap is not None:
        return resource_container.ConceptMap
    if resource_container.Condition is not None:
        return resource_container.Condition
    if resource_container.Consent is not None:
        return resource_container.Consent
    if resource_container.Contract is not None:
        return resource_container.Contract
    if resource_container.Coverage is not None:
        return resource_container.Coverage
    if resource_container.CoverageEligibilityRequest is not None:
        return resource_container.CoverageEligibilityRequest
    if resource_container.CoverageEligibilityResponse is not None:
        return resource_container.CoverageEligibilityResponse
    if resource_container.DetectedIssue is not None:
        return resource_container.DetectedIssue
    if resource_container.Device is not None:
        return resource_container.Device
    if resource_container.DeviceDefinition is not None:
        return resource_container.DeviceDefinition
    if resource_container.DeviceMetric is not None:
        return resource_container.DeviceMetric
    if resource_container.DeviceRequest is not None:
        return resource_container.DeviceRequest
    if resource_container.DeviceUseStatement is not None:
        return resource_container.DeviceUseStatement
    if resource_container.DiagnosticReport is not None:
        return resource_container.DiagnosticReport
    if resource_container.DocumentManifest is not None:
        return resource_container.DocumentManifest
    if resource_container.DocumentReference is not None:
        return resource_container.DocumentReference
    if resource_container.Encounter is not None:
        return resource_container.Encounter
    if resource_container.Endpoint is not None:
        return resource_container.Endpoint
    if resource_container.EnrollmentRequest is not None:
        return resource_container.EnrollmentRequest
    if resource_container.EnrollmentResponse is not None:
        return resource_container.EnrollmentResponse
    if resource_container.EpisodeOfCare is not None:
        return resource_container.EpisodeOfCare
    if resource_container.EventDefinition is not None:
        return resource_container.EventDefinition
    if resource_container.Evidence is not None:
        return resource_container.Evidence
    if resource_container.EvidenceReport is not None:
        return resource_container.EvidenceReport
    if resource_container.EvidenceVariable is not None:
        return resource_container.EvidenceVariable
    if resource_container.ExampleScenario is not None:
        return resource_container.ExampleScenario
    if resource_container.ExplanationOfBenefit is not None:
        return resource_container.ExplanationOfBenefit
    if resource_container.FamilyMemberHistory is not None:
        return resource_container.FamilyMemberHistory
    if resource_container.Flag is not None:
        return resource_container.Flag
    if resource_container.Goal is not None:
        return resource_container.Goal
    if resource_container.GraphDefinition is not None:
        return resource_container.GraphDefinition
    if resource_container.Group is not None:
        return resource_container.Group
    if resource_container.GuidanceResponse is not None:
        return resource_container.GuidanceResponse
    if resource_container.HealthcareService is not None:
        return resource_container.HealthcareService
    if resource_container.ImagingStudy is not None:
        return resource_container.ImagingStudy
    if resource_container.Immunization is not None:
        return resource_container.Immunization
    if resource_container.ImmunizationEvaluation is not None:
        return resource_container.ImmunizationEvaluation
    if resource_container.ImmunizationRecommendation is not None:
        return resource_container.ImmunizationRecommendation
    if resource_container.ImplementationGuide is not None:
        return resource_container.ImplementationGuide
    if resource_container.Ingredient is not None:
        return resource_container.Ingredient
    if resource_container.InsurancePlan is not None:
        return resource_container.InsurancePlan
    if resource_container.Invoice is not None:
        return resource_container.Invoice
    if resource_container.Library is not None:
        return resource_container.Library
    if resource_container.Linkage is not None:
        return resource_container.Linkage
    if resource_container.List is not None:
        return resource_container.List
    if resource_container.Location is not None:
        return resource_container.Location
    if resource_container.ManufacturedItemDefinition is not None:
        return resource_container.ManufacturedItemDefinition
    if resource_container.Measure is not None:
        return resource_container.Measure
    if resource_container.MeasureReport is not None:
        return resource_container.MeasureReport
    if resource_container.Media is not None:
        return resource_container.Media
    if resource_container.Medication is not None:
        return resource_container.Medication
    if resource_container.MedicationAdministration is not None:
        return resource_container.MedicationAdministration
    if resource_container.MedicationDispense is not None:
        return resource_container.MedicationDispense
    if resource_container.MedicationKnowledge is not None:
        return resource_container.MedicationKnowledge
    if resource_container.MedicationRequest is not None:
        return resource_container.MedicationRequest
    if resource_container.MedicationStatement is not None:
        return resource_container.MedicationStatement
    if resource_container.MedicinalProductDefinition is not None:
        return resource_container.MedicinalProductDefinition
    if resource_container.MessageDefinition is not None:
        return resource_container.MessageDefinition
    if resource_container.MessageHeader is not None:
        return resource_container.MessageHeader
    if resource_container.MolecularSequence is not None:
        return resource_container.MolecularSequence
    if resource_container.NamingSystem is not None:
        return resource_container.NamingSystem
    if resource_container.NutritionOrder is not None:
        return resource_container.NutritionOrder
    if resource_container.NutritionProduct is not None:
        return resource_container.NutritionProduct
    if resource_container.Observation is not None:
        return resource_container.Observation
    if resource_container.ObservationDefinition is not None:
        return resource_container.ObservationDefinition
    if resource_container.OperationDefinition is not None:
        return resource_container.OperationDefinition
    if resource_container.OperationOutcome is not None:
        return resource_container.OperationOutcome
    if resource_container.Organization is not None:
        return resource_container.Organization
    if resource_container.OrganizationAffiliation is not None:
        return resource_container.OrganizationAffiliation
    if resource_container.PackagedProductDefinition is not None:
        return resource_container.PackagedProductDefinition
    if resource_container.Patient is not None:
        return resource_container.Patient
    if resource_container.PaymentNotice is not None:
        return resource_container.PaymentNotice
    if resource_container.PaymentReconciliation is not None:
        return resource_container.PaymentReconciliation
    if resource_container.Person is not None:
        return resource_container.Person
    if resource_container.PlanDefinition is not None:
        return resource_container.PlanDefinition
    if resource_container.Practitioner is not None:
        return resource_container.Practitioner
    if resource_container.PractitionerRole is not None:
        return resource_container.PractitionerRole
    if resource_container.Procedure is not None:
        return resource_container.Procedure
    if resource_container.Provenance is not None:
        return resource_container.Provenance
    if resource_container.Questionnaire is not None:
        return resource_container.Questionnaire
    if resource_container.QuestionnaireResponse is not None:
        return resource_container.QuestionnaireResponse
    if resource_container.RegulatedAuthorization is not None:
        return resource_container.RegulatedAuthorization
    if resource_container.RelatedPerson is not None:
        return resource_container.RelatedPerson
    if resource_container.RequestGroup is not None:
        return resource_container.RequestGroup
    if resource_container.ResearchDefinition is not None:
        return resource_container.ResearchDefinition
    if resource_container.ResearchElementDefinition is not None:
        return resource_container.ResearchElementDefinition
    if resource_container.ResearchStudy is not None:
        return resource_container.ResearchStudy
    if resource_container.ResearchSubject is not None:
        return resource_container.ResearchSubject
    if resource_container.RiskAssessment is not None:
        return resource_container.RiskAssessment
    if resource_container.Schedule is not None:
        return resource_container.Schedule
    if resource_container.SearchParameter is not None:
        return resource_container.SearchParameter
    if resource_container.ServiceRequest is not None:
        return resource_container.ServiceRequest
    if resource_container.Slot is not None:
        return resource_container.Slot
    if resource_container.Specimen is not None:
        return resource_container.Specimen
    if resource_container.SpecimenDefinition is not None:
        return resource_container.SpecimenDefinition
    if resource_container.StructureDefinition is not None:
        return resource_container.StructureDefinition
    if resource_container.StructureMap is not None:
        return resource_container.StructureMap
    if resource_container.Subscription is not None:
        return resource_container.Subscription
    if resource_container.SubscriptionStatus is not None:
        return resource_container.SubscriptionStatus
    if resource_container.SubscriptionTopic is not None:
        return resource_container.SubscriptionTopic
    if resource_container.Substance is not None:
        return resource_container.Substance
    if resource_container.SubstanceDefinition is not None:
        return resource_container.SubstanceDefinition
    if resource_container.SupplyDelivery is not None:
        return resource_container.SupplyDelivery
    if resource_container.SupplyRequest is not None:
        return resource_container.SupplyRequest
    if resource_container.Task is not None:
        return resource_container.Task
    if resource_container.TerminologyCapabilities is not None:
        return resource_container.TerminologyCapabilities
    if resource_container.TestReport is not None:
        return resource_container.TestReport
    if resource_container.TestScript is not None:
        return resource_container.TestScript
    if resource_container.ValueSet is not None:
        return resource_container.ValueSet
    if resource_container.VerificationResult is not None:
        return resource_container.VerificationResult
    if resource_container.VisionPrescription is not None:
        return resource_container.VisionPrescription
    if resource_container.Parameters is not None:
        return resource_container.Parameters
    return None

default_types_maps = {
    (malac.models.cda.at_ext.II, malac.models.fhir.r4.Identifier): II,
    (malac.models.cda.at_ext.INT, malac.models.fhir.r4.integer): INT,
    (malac.models.cda.at_ext.BL, malac.models.fhir.r4.boolean): BL,
    (malac.models.cda.at_ext.TS, malac.models.fhir.r4.instant): TSInstant,
    (malac.models.cda.at_ext.IVL_TS, malac.models.fhir.r4.instant): IVL_TSDateTime,
    (malac.models.cda.at_ext.TS, malac.models.fhir.r4.dateTime): TSDateTime,
    (malac.models.cda.at_ext.IVXB_TS, malac.models.fhir.r4.dateTime): IVXB_TSDateTime,
    (malac.models.cda.at_ext.TS, malac.models.fhir.r4.date): TSDate,
    (malac.models.cda.at_ext.IVL_TS, malac.models.fhir.r4.Period): IVLTSPeriod,
    (malac.models.cda.at_ext.IVL_TS, malac.models.fhir.r4.dateTime): IVLTSDateTime,
    (malac.models.cda.at_ext.ST, malac.models.fhir.r4.string): STstring,
    (malac.models.cda.at_ext.ED, malac.models.fhir.r4.string): EDstring,
    (malac.models.cda.at_ext.EN, malac.models.fhir.r4.string): ENstring,
    (malac.models.cda.at_ext.ON, malac.models.fhir.r4.string): ONstring,
    (malac.models.cda.at_ext.CS, malac.models.fhir.r4.code): CSCode,
    (malac.models.cda.at_ext.CE, malac.models.fhir.r4.code): CECode,
    (malac.models.cda.at_ext.CD, malac.models.fhir.r4.code): CDCode,
    (malac.models.cda.at_ext.CE, malac.models.fhir.r4.Coding): CECoding,
    (malac.models.cda.at_ext.CD, malac.models.fhir.r4.Coding): CDCoding,
    (malac.models.cda.at_ext.CE, malac.models.fhir.r4.CodeableConcept): CECodeableConcept,
    (malac.models.cda.at_ext.CS, malac.models.fhir.r4.CodeableConcept): CSCodeableConcept,
    (malac.models.cda.at_ext.CD, malac.models.fhir.r4.CodeableConcept): CDCodeableConcept,
    (malac.models.cda.at_ext.PN, malac.models.fhir.r4.HumanName): CdaPersonNameCompilationToFhirHumanName,
    (malac.models.cda.at_ext.AD, malac.models.fhir.r4.Address): CdaAdressCompilationToFhirAustrianAddress,
    (malac.models.cda.at_ext.TEL, malac.models.fhir.r4.ContactPoint): TELContactPoint,
    (malac.models.cda.at_ext.PQ, malac.models.fhir.r4.Quantity): PQQuantity,
    (malac.models.cda.at_ext.IVL_PQ, malac.models.fhir.r4.Range): IVLPQRange,
    (malac.models.cda.at_ext.IVXB_PQ, malac.models.fhir.r4.Quantity): IVXB_PQQuantity,
    (malac.models.cda.at_ext.RTO_PQ_PQ, malac.models.fhir.r4.Ratio): RTOPQPQRatio,
}
default_types_maps_plus = {
}

def transform_default(source, target, target_type=None):
    target_type = target_type or type(target)
    source_type = type(source)
    while source_type is not None:
        default_map = default_types_maps.get((source_type, target_type))
        if default_map:
            default_map(source, target)
            return
        source_type = source_type.__bases__[0] if source_type.__bases__ else None
    source_type = type(source)
    while source_type is not None:
        default_map_plus = default_types_maps_plus.get(source_type)
        if default_map_plus:
            default_map_plus(source, target)
            return
        source_type = source_type.__bases__[0] if source_type.__bases__ else None
    raise BaseException('No default transform found for %s -> %s' % (type(source), target_type))

def translate_unmapped(url, code):
    if url == 'http://hl7.org/fhir/ConceptMap/special-oid2uri': return [{'uri': 'urn:oid:%s' % code}]
    if url == 'OIDtoURI': return [{'code': 'urn:oid:%s' % code}]
    if url == 'StructureMapGroupTypeMode': return [{'code': 'none'}]
    if url == 'AllergyCategoryMap': return [{'code': None}]
    raise BaseException('Code %s could not be mapped to any code in concept map %s and no exception defined' % (code, url))

def translate_single(url, code, out_type):
    trans_out = translate(url=url, code=code, silent=True)
    matches = [match['concept'] for match in trans_out['match'] if match['relationship']=='equivalent' or match['relationship']=='equal']
    # if there are mutliple 'equivalent' or 'equal' matches and CodeableConcept is not the output param, than throw an error
    if len(matches) > 1:
        raise BaseException("There are multiple 'equivalent' or 'equal' matches in the results of the translate and output type is not CodeableConcept!")
    elif len(matches) == 0:
        matches = translate_unmapped(url=url, code=code)
    if out_type == "Coding":
        return malac.models.fhir.r4.Coding(system=(malac.models.fhir.r4.uri(value=matches[0]['system']) if "system" in matches[0] else None), 
                              version=(malac.models.fhir.r4.string(value=matches[0]['version']) if "version" in matches[0] else None), 
                              code=(malac.models.fhir.r4.string(value=matches[0]['code']) if "code" in matches[0] else None), 
                              display=(malac.models.fhir.r4.string(value=matches[0]['display']) if "display" in  matches[0] else None), 
                              userSelected=(malac.models.fhir.r4.string(value=matches[0]['userSelected']) if "userSelected" in matches[0] else None))
    else:
        return matches[0][out_type]

def translate_multi(url, code):
    trans_out = translate(url=url, code=code, silent=True)
    matches = [match['concept'] for match in trans_out['match'] if match['relationship']=='equivalent' or match['relationship']=='equal']
    return malac.models.fhir.r4.CodeableConcept(coding=[malac.models.fhir.r4.Coding(system=(malac.models.fhir.r4.uri(value=matches[0]['system']) if "system" in matches[0] else None), 
                                                          version=(malac.models.fhir.r4.string(value=matches[0]['version']) if "version" in matches[0] else None), 
                                                          code=(malac.models.fhir.r4.string(value=matches[0]['code']) if "code" in matches[0] else None), 
                                                          display=(malac.models.fhir.r4.string(value=matches[0]['display']) if "display" in  matches[0] else None), 
                                                          userSelected=(malac.models.fhir.r4.string(value=matches[0]['userSelected']) if "userSelected" in matches[0] else None)
                                                          ) for match in matches])


if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()
    transform(args.source, args.target)
