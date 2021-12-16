#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 18:55:23 2020
@author: CE
"""


import pandas as pd
from rdflib import Graph, Literal, RDF, Namespace, URIRef
from rdflib.namespace import RDFS, FOAF
from SPARQLWrapper import SPARQLWrapper, N3
from lxml import etree
import re
"""Import libraries."""

crm=Namespace('http://www.cidoc-crm.org/cidoc-crm/')
"""Defines namespace for CIDOC CRM."""
ex=Namespace('https://www.intavia.org/')
"""Defines namespace for own ontology."""
idm=Namespace('https://www.intavia.org/idm/')
"""Defines namespace for own ontology."""
ore=Namespace('http://www.openarchives.org/ore/terms/')
"""Defines namespace for schema.org vocabulary."""
edm=Namespace('http://www.europeana.eu/schemas/edm/')
"""Defines namespace for Europeana data model vocabulary."""
ore=Namespace('http://www.openarchives.org/ore/terms/')
"""Defines namespace for Europeana data model vocabulary."""
owl=Namespace('http://www.w3.org/2002/07/owl#')
"""Defines namespace for Europeana data model vocabulary."""
rdf=Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
"""Defines namespace for Europeana data model vocabulary."""
xml=Namespace('http://www.w3.org/XML/1998/namespace')
"""Defines namespace for Europeana data model vocabulary."""
xsd=Namespace('http://www.w3.org/2001/XMLSchema#')
"""Defines namespace for Europeana data model vocabulary."""
bioc=Namespace('http://www.ldf.fi/schema/bioc/')
"""Defines namespace for Europeana data model vocabulary."""
rdfs=Namespace('http://www.w3.org/2000/01/rdf-schema#')
"""Defines namespace for Europeana data model vocabulary."""
apis=Namespace('https://www.apis.acdh.oeaw.ac.at/')
"""Defines namespace for APIS database."""
owl=Namespace('http://www.w3.org/2002/07/owl#')
"""Defines OWL namespace."""

pldf = pd.read_csv("persons.csv", sep=",", quotechar='"', encoding='utf-8')
"""Read CSV in Pandas Dataframe."""

chodf = pd.read_csv("cho.csv", sep=",", quotechar='"', encoding='utf-8')

pldf.columns = ['intavia_id', 'forename', 'surname', 'birthdate', 'birthplace', 'deathdate', 'deathplace', 'occupation_general', 'gender', 'nationality','sibling_forename','sibling_surname','source_dataset_id','source_dataset','source_responsible_institution']

chodf.columns = ['intavia_id', 'cho_id', 'creator','contributor','date','cdate','mediumI','mediumII','mediumIII','mediumIV','mediumV','mediumVI','mediumVII','mediumVIII','extent','currentLocation','dcidentifierI','dcidentifierII','providerproxy','providedcho','mf','aggregation','dp','rights','title','coverage','creation','description','relation','subjectI','subjectII','subjectIII','subjectIV','subjectV','typeI','typeII','typeIII','typeIV','typeV','typeVII','typeVIII','typeIX','typeX','language','carrieslinguistic']

pldf = pldf.applymap(str)
"""Convert all items in the Personlistdataframe to strings."""
chodf = chodf.applymap(str)

def medium_triple(med, cho_id, columntitle):
    """Triples for medium of CHO"""
    if med != "nan":
        if med.startswith('http'):
            g.add((URIRef(ex+'choproxy/'+row['cho_id']), crm.P45_consists_of, (URIRef(med))))
        else:
            g.add((URIRef(ex+'choproxy/'+row['cho_id']), crm.P45_consists_of, (URIRef(ex+'medium/'+columntitle+'/'+cho_id))))
            g.add((URIRef(ex+'medium/'+columntitle+'/'+cho_id), rdfs.label, Literal(med)))

def type_triple(type, cho_id, columntitle):
    """Triples for type of CHO"""
    if type != "nan":
        if type.startswith('http'):
            g.add((URIRef(ex+'production_event/'+row['cho_id']), crm.P32_used_general_technique, (URIRef(type))))
            g.add((URIRef(type), RDF.type, crm.E55_Type))
            g.add((crm.E55_Type , rdfs.label , Literal('Type')))
        else:
            g.add((URIRef(ex+'production_event/'+row['cho_id']), crm.P32_used_general_technique, (URIRef(ex+'type/'+columntitle+'/'+cho_id))))
            g.add((URIRef(ex+'type/'+columntitle+'/'+cho_id), RDF.type, crm.E55_Type))
            g.add((crm.E55_Type , rdfs.label , Literal('Type')))
            g.add((URIRef(ex+'type/'+columntitle+'/'+cho_id), rdfs.label, Literal(type)))

def subject_triple(subject, cho_id, columntitle):
    """Triples for subject of CHO"""
    if subject != "nan":
        if subject.startswith('http'):
            g.add((URIRef(ex+'choproxy/'+row['cho_id']), crm.P62_depicts, (URIRef(subject))))
            g.add((URIRef(subject), RDF.type, crm.E1_CRM_Entity))
            g.add((crm.E1_CRM_Entity , rdfs.label , Literal('CRM Entity')))
        else:
            g.add((URIRef(ex+'choproxy/'+row['cho_id']), crm.P62_depicts, (URIRef(ex+'subject/'+columntitle+'/'+cho_id))))
            g.add((URIRef(ex+'subject/'+columntitle+'/'+cho_id), RDF.type, crm.E1_CRM_Entity))
            g.add((crm.E1_CRM_Entity , rdfs.label , Literal('CRM Entity')))
            g.add((URIRef(ex+'type/'+columntitle+'/'+cho_id), rdfs.label, Literal(subject)))


g = Graph()
#Create undirected graph, assigned to g
 
for index, row in pldf.iterrows():
    """Create RDF Triples, according to IDM data model."""
    g.add((URIRef(ex+'providedperson/'+row['intavia_id']), RDF.type, idm.Provided_Person))
    g.add((idm.Provided_Person , rdfs.label , Literal('IDM Provided Person')))
    """Initialize URI for Provided Person"""
    g.add((URIRef(ex+'personproxy/'+row['source_dataset_id']+'/'+row['intavia_id']), idm.person_proxy_for, URIRef(ex+'providedperson/'+row['intavia_id'])))
    """add person proxy to person"""
    g.add((URIRef(ex+'personproxy/'+row['source_dataset_id']+'/'+row['intavia_id']), RDF.type, idm.Person_Proxy))
    g.add((idm.Person_Proxy , rdfs.label , Literal('IDM Person Proxy')))
    g.add((URIRef(ex+'personproxy/'+row['source_dataset_id']+'/'+row['intavia_id']), RDF.type, crm.E21_Person))
    g.add((crm.E21_Person , rdfs.label , Literal('Person')))
    """declare Person_Proxy and CRM E21 Person"""
    g.add((URIRef(ex+'personproxy/'+row['source_dataset_id']+'/'+row['intavia_id']), crm.P1_is_identified_by, (URIRef(idm+'personid/'+row['source_dataset']+'/'+row['source_dataset_id']))))
    """Add Source Dataset Identifier for Statement to Person Proxy"""
    g.add((URIRef(ex+'personid/'+row['source_dataset']+'/'+row['source_dataset_id']), crm.P2_has_type, ((URIRef(ex+'personid/'+row['source_dataset'])))))
    """information about source dataset"""
    g.add((URIRef(ex+'personid/'+row['source_dataset']), rdfs.label, (Literal(row['source_dataset']))))
    """add label to source dataset"""
    g.add((URIRef(ex+'personid/'+row['source_dataset_id']), RDF.type, crm.E42_Identifier))
    g.add((crm.E42_Identifier , rdfs.label , Literal('Identifier')))
    """define specific Source Dataset ID as Identifier"""
    g.add((URIRef(ex+'personid/'+row['source_dataset_id']), rdfs.label, (Literal(row['source_dataset_id']))))
    """add human-readable value of Source Dataset ID"""
    #g.add((URIRef(ex+'personid/'+row['source_dataset_id']), crm.P2_has_type, (URIRef(ex+'idtype/'+row['id_type']))))
    #"""define type of Identifier"""
    #g.add((URIRef(ex+'idtype/'+row['id_type']), rdfs.label, (Literal('Source Dataset Identifier'))))
    #"""add human-readable id type"""
    #g.add((URIRef(ex+'idtype/'+row['id_type']), RDF.type, crm.E55_Type))
    #"""declare CRM E55 Type"""
    #identifierassignment
    g.add((URIRef(ex+'identassig/'+row['intavia_id']), RDF.type, crm.E15_Identifier_Assignment))
    g.add((crm.E15_Identifier_Assignment , rdfs.label , Literal('Identifier Assignment')))
    """defined event as Identifier Assignment"""
    g.add((URIRef(ex+'identassig/'+row['intavia_id']), crm.P37_assigned, (URIRef(apis+'personid/'+row['source_dataset_id']))))
    """Identifier Assignment assigned Identifier"""
    g.add((URIRef(ex+'identassig/'+row['intavia_id']), bioc.had_participant_in_role, (URIRef(ex+'role/'+'ResponsibleForIdentifier'+'/'+row['intavia_id']))))
    """Identifier Assignment had participant in role ResponsibleForIdentifier"""
    g.add((URIRef(ex+'role/'+'ResponsibleForIdentifier'+'/'+row['intavia_id']), RDF.type, bioc.Event_Role))
    g.add((bioc.Event_Role , rdfs.label , Literal('Event Role')))
    """assigned role as an event role"""
    g.add((URIRef(ex+'role/'+'ResponsibleForIdentifier'+'/'+row['intavia_id']), rdfs.label, (Literal('responsible Actor'))))
    """add human-readable role for identifier assignment event"""
    g.add((URIRef(ex+'institution/'+row['source_responsible_institution']), bioc.bearer_of, (URIRef(idm+'role/'+'ResponsibleForIdentifier'+'/'+row['intavia_id']))))
    """defines who is responsible for the identifier assignment"""
    g.add((URIRef(ex+'institution/'+row['source_responsible_institution']), bioc.bearer_of, (URIRef(idm+'role/'+'ResponsibleForIdentifier'+'/'+row['intavia_id']))))
    """add human-readable label for responsible institution"""
    #name
    g.add((URIRef(ex+'personproxy/'+row['source_dataset_id']+'/'+row['intavia_id']), crm.P1_is_identified_by, (URIRef(ex+'name/'+'1/'+row['source_dataset_id']+row['intavia_id']))))
    """add name to Person Proxy"""
    g.add((URIRef(ex+'name/'+'1/'+row['source_dataset_id']+row['intavia_id']), RDF.type, crm.E33_E41_Linguistic_Appellation))
    g.add((crm.E33_E41_Linguistic_Appellation , rdfs.label , Literal('Linguistic Appellation')))
    """defines name as Cidoc E33_E41_Linguistic_Appellation"""
    g.add((URIRef(ex+'name/'+'2/'+row['source_dataset_id']+row['intavia_id']), RDF.type, crm.E33_E41_Linguistic_Appellation))
    """defines name as Cidoc E33_E41_Linguistic_Appellation"""
    g.add((URIRef(ex+'name/'+'3/'+row['source_dataset_id']+row['intavia_id']), RDF.type, crm.E33_E41_Linguistic_Appellation))
    """defines name as Cidoc E33_E41_Linguistic_Appellation"""
    #surname
    g.add((URIRef(ex+'name/'+'1/'+row['source_dataset_id']+row['intavia_id']), crm.P148_has_component, (URIRef(ex+'name/'+'2/'+row['source_dataset_id']+row['intavia_id']))))
    """add surname"""
    g.add((URIRef(ex+'name/'+'2/'+row['source_dataset_id']+row['intavia_id']), crm.P2_has_type, (URIRef(ex+'nametype/'+'surname'))))
    """define as type surname"""
    g.add((URIRef(ex+'nametype/'+'surname'), rdfs.label, (Literal('surname'))))
    """add human-readable label for nametype"""
    g.add((URIRef(ex+'name/'+'2/'+row['source_dataset_id']+row['intavia_id']), rdfs.value , (Literal(row['surname']))))
    """add string for surname"""
    #forename
    g.add((URIRef(ex+'name/'+'1/'+row['source_dataset_id']+row['intavia_id']), crm.P148_has_component, (URIRef(ex+'name/'+'3/'+row['source_dataset_id']+row['intavia_id']))))
    """add forename"""
    g.add((URIRef(ex+'name/'+'3/'+row['source_dataset_id']+row['intavia_id']), crm.P2_has_type, (URIRef(ex+'nametype/'+'forename'))))
    """define as type forename"""
    g.add((URIRef(ex+'nametype/'+'forename'), rdfs.label, (Literal('forename'))))
    """add human-readable label for nametype"""
    g.add((URIRef(ex+'name/'+'3/'+row['source_dataset_id']+row['intavia_id']), rdfs.value, (Literal(row['forename']))))
    """add string for surname"""
    #birth
    g.add((URIRef(ex+'birthevent/'+row['intavia_id']), crm.P98_brought_into_life, (URIRef(ex+'personproxy/'+row['source_dataset_id']+'/'+row['intavia_id']))))
    """adds birth event to Person Proxy"""
    g.add((URIRef(ex+'birthevent/'+row['intavia_id']), RDF.type, crm.E67_Birth))
    g.add((crm.E67_Birth , rdfs.label , Literal('Birth')))
    """defines event as Cidoc Birth Event"""
    g.add((URIRef(ex+'birthevent/'+row['intavia_id']), crm.P4_has_time_span, (URIRef(ex+'timespan/'+'1/'+row['intavia_id']))))
    """time span for birth event"""
    g.add((URIRef(ex+'timespan/'+'1/'+row['intavia_id']), RDF.type, crm.E52_Time_Span))
    g.add((crm.E52_Time_Span, rdfs.label , Literal('Time-Span')))
    """defines specific time-span as class E52 Time Span"""
    g.add((URIRef(ex+'timespan/'+'1/'+row['intavia_id']), crm.P81a_begin_of_the_begin, (Literal(row['birthdate'])+'+00:00:00')))
    """defines begin of birthdate"""
    g.add((URIRef(ex+'timespan/'+'1/'+row['intavia_id']), crm.P82b_end_of_the_end, (Literal(row['birthdate'])+'+23:59:59')))
    """defines begin of birthdate"""
    #death
    g.add((URIRef(ex+'deathevent/'+row['intavia_id']), crm.P100_was_death_of, (URIRef(ex+'personproxy/'+row['source_dataset_id']+'/'+row['intavia_id']))))
    """adds death event to Person Proxy"""
    g.add((URIRef(ex+'deathevent/'+row['intavia_id']), RDF.type, crm.E69_Death))
    g.add((crm.E69_Death, rdfs.label , Literal('Death')))
    """defines event as Cidoc Death Event"""
    g.add((URIRef(ex+'deathevent/'+row['intavia_id']), crm.P4_has_time_span, (URIRef(ex+'timespan/'+'2/'+row['intavia_id']))))
    """time span for death event"""
    g.add((URIRef(ex+'timespan/'+'2/'+row['intavia_id']), crm.P81a_begin_of_the_begin, (Literal(row['deathdate'])+'+00:00:00')))
    """defines begin of deathdate"""
    g.add((URIRef(ex+'timespan/'+'2/'+row['intavia_id']), RDF.type, crm.E52_Time_Span))
    g.add((crm.E52_Time_Span, rdfs.label , Literal('Time-Span')))
    """defines specific time-span as class E52 Time Span"""
    g.add((URIRef(ex+'timespan/'+'2/'+row['intavia_id']), crm.P82b_end_of_the_end, (Literal(row['deathdate'])+'+23:59:59')))
    """defines end of deathdate"""
    #gender
    g.add((URIRef(ex+'personproxy/'+row['source_dataset_id']+'/'+row['intavia_id']), bioc.has_gender, (URIRef(bioc+row['gender']))))
    """defines gender of Person_Proxy"""
    g.add((URIRef(bioc+row['gender']), rdfs.label, (Literal(row['gender']))))
    """add human-readable label to gender"""
    g.add((URIRef(bioc+row['gender']), RDF.type, bioc.Gender))
    g.add((bioc.Gender, rdfs.label , Literal('Gender')))
    """define Gender as biocrm gender"""
    #occupation
    g.add((URIRef(ex+'personproxy/'+row['source_dataset_id']+'/'+row['intavia_id']), bioc.has_occupation, (URIRef(bioc+row['occupation_general']))))
    """add occupation to Person Proxy"""
    g.add((URIRef(bioc+row['occupation_general']), rdfs.label, (Literal(row['occupation_general']))))
    """add human-readable label to general occupation"""
    g.add((URIRef(bioc+row['occupation_general']), RDF.type, bioc.Occupation))
    g.add((bioc.Occupation, rdfs.label , Literal('Occupation')))
    """define occupation as biocrm occupation"""
    #nationality
    g.add((URIRef(ex+'personproxy/'+row['source_dataset_id']+'/'+row['intavia_id']), bioc.has_nationality, (URIRef(bioc+row['nationality']))))
    """add nationality to Person Proxy"""
    g.add((URIRef(bioc+row['nationality']), rdfs.label, (Literal(row['nationality']))))
    """add human-readable label to nationality"""
    g.add((URIRef(bioc+row['nationality']), RDF.type, bioc.Nationality))
    g.add((bioc.Nationality, rdfs.label , Literal('Nationality')))
    """define nationality as biocrm nationality"""
    #family relation
    if (row['sibling_surname']) != "nan":
        g.add((URIRef(ex+'personproxy/'+row['source_dataset_id']+'/'+row['intavia_id']), bioc.has_family_relation, (URIRef(ex+'familyrelation/'+'1/'+row['intavia_id']))))
        """add family relation"""
        g.add((URIRef(ex+'familyrelation/'+'1/'+'/'+row['intavia_id']), RDF.type, bioc.Family_Relationship_Role))
        g.add((bioc.Family_Relationship_Role, rdfs.label , Literal('Family Relationship Role')))
        """family relationship role is from Bioc"""
        g.add((URIRef(ex+'familyrelation/'+'1/'+'/'+row['intavia_id']), crm.P2_has_type, (URIRef(ex+'familyreltype/'+'sibling'))))
        """add type of family relation"""
        g.add((URIRef(ex+'familyreltype/'+'sibling'), rdfs.label, Literal('Sibling')))
        """add human-readable label to sibling type"""
        g.add((URIRef(ex+'familyrelation/'+'1/'+'/'+row['intavia_id']), bioc.inheres_in, (URIRef(ex+'personproxy/'+row['sibling_forename']+row['sibling_surname']))))
        """points to second person in family relation"""
        g.add((URIRef(ex+'person/'+row['sibling_forename']+row['sibling_surname']), RDF.type, idm.Provided_Person))
        g.add((bioc.Provided_Person, rdfs.label , Literal('IDM Provided Person')))
        g.add((URIRef(ex+'personproxy/'+row['sibling_forename']+row['sibling_surname']), RDF.type, idm.Person_Proxy))
        g.add((idm.Person_Proxy, rdfs.label , Literal('IDM Person Proxy')))
        g.add((URIRef(ex+'personproxy/'+row['sibling_forename']+row['sibling_surname']), RDF.type, crm.E21_Person))
        g.add((crm.E21_Person, rdfs.label , Literal('Person')))
        g.add((URIRef(ex+'personproxy/'+row['sibling_forename']+row['sibling_surname']), idm.person_proxy_for, (URIRef(ex+'person/'+row['sibling_forename']+row['sibling_surname']))))
        """defines sibling as person"""
        g.add((URIRef(ex+'personproxy/'+row['sibling_forename']+row['sibling_surname']), crm.P1_is_identified_by, (URIRef(ex+'name/'+'1/'+row['sibling_forename']+row['sibling_surname']))))
        """add name to Person Proxy"""
        g.add((URIRef(ex+'name/'+'1/'+row['sibling_forename']+row['sibling_surname']), RDF.type, crm.E41_E33_Linguistic_Appellation))
        g.add((crm.E41_E33_Linguistic_Appellation, rdfs.label , Literal('Linguistic Appellation')))
        """defines name as Cidoc E41 Appellation"""
        g.add((URIRef(ex+'name/'+'1/'+row['sibling_forename']+row['sibling_surname']), crm.P148_has_component, (URIRef(ex+'name/'+'2/'+row['sibling_forename']+row['sibling_surname']))))
        """add surname"""
        g.add((URIRef(ex+'name/'+'2/'+row['sibling_forename']+row['sibling_surname']), RDF.type, crm.E41_E33_Linguistic_Appellation))
        """defines surname as Cidoc E41 Appellation"""
        g.add((URIRef(ex+'name/'+'2/'+row['sibling_forename']+row['sibling_surname']), crm.P2_has_type, (URIRef(ex+'nametype/'+'surname'))))
        """define as type surname"""
        g.add((URIRef(ex+'name/'+'2/'+row['sibling_forename']+row['sibling_surname']), rdfs.value , (Literal(row['sibling_surname']))))
        """add string for surname"""
        g.add((URIRef(ex+'name/'+'1/'+row['sibling_forename']+row['sibling_surname']), crm.P148_has_component, (URIRef(ex+'name/'+'3/'+row['sibling_forename']+row['sibling_surname']))))
        """add forename"""
        g.add((URIRef(ex+'name/'+'3/'+row['sibling_forename']+row['sibling_surname']), RDF.type, crm.E41_E33_Linguistic_Appellation))
        """defines forename as Cidoc crm.E41_E33_Linguistic_Appellation"""
        g.add((URIRef(ex+'name/'+'3/'+row['sibling_forename']+row['sibling_surname']), crm.P2_has_type, (URIRef(ex+'nametype/'+'forename'))))
        """define as type forename"""
        g.add((URIRef(ex+'name/'+'3/'+row['sibling_forename']+row['sibling_surname']), rdfs.value, (Literal(row['sibling_forename']))))
        """add string for forename"""

for index, row in chodf.iterrows():
    g.add((URIRef(ex+'personproxy/'+'europeana/'+row['intavia_id']), idm.person_proxy_for, URIRef(ex+'providedperson/'+row['intavia_id'])))
    """add person proxy to person"""
    g.add((URIRef(ex+'personproxy/'+'europeana/'+row['intavia_id']), RDF.type, idm.Person_Proxy))
    g.add((idm.Person_Proxy, rdfs.label , Literal('IDM Person Proxy')))
    g.add((URIRef(ex+'personproxy/'+'europeana/'+row['intavia_id']), RDF.type, crm.E21_Person))
    """declare Person_Proxy and CRM E21 Person"""
    g.add((URIRef(ex+'production_event/'+row['cho_id']), RDF.type, crm.E12_Production))
    g.add((crm.E12_Production, rdfs.label , Literal('Production')))
    """define production event"""
    g.add((URIRef(ex+'cho/'+row['cho_id']), RDF.type, idm.Provided_CHO))
    g.add((idm.Provided_CHO, rdfs.label , Literal('IDM Provided CHO')))
    """define provided cho"""
    g.add((URIRef(ex+'choproxy/'+row['cho_id']), idm.cho_proxy_for, (URIRef(ex+'cho/'+row['cho_id']))))
    """define proxy for provided cho"""
    g.add((URIRef(ex+'choproxy/'+row['cho_id']), RDF.type, idm.CHO_Proxy))
    g.add((idm.CHO_Proxy, rdfs.label , Literal('IDM CHO Proxy')))
    g.add((URIRef(ex+'choproxy/'+row['cho_id']), RDF.type, crm.E18_Physical_Thing))
    g.add((crm.E18_Physical_Thing, rdfs.label , Literal('Physical Thing')))
    g.add((URIRef(ex+'production_event/'+row['cho_id']), bioc.occured_in_the_presence_of_in_role, (URIRef(ex+'productionthingrole/'+row['cho_id']))))
    """adds thingrole to productionevent"""
    g.add((URIRef(ex+'productionthingrole/'+row['cho_id']), RDF.type, bioc.Thing_Role))
    g.add((bioc.Thing_Role, rdfs.label , Literal('Thing Role')))
    g.add((URIRef(ex+'productionthingrole/'+row['cho_id']), crm.P12_occurred_in_the_presence_of, (URIRef(ex+'choproxy/'+row['cho_id']))))
    """connects production event and cho proxy"""
    g.add((URIRef(ex+'production_event/'+row['cho_id']), crm.P4_has_time_span, (URIRef(ex+'timespan/'+'1/'+row['cho_id']))))
    g.add((URIRef(ex+'timespan/'+'1/'+row['cho_id']), RDF.type, crm.E52_Time_Span))
    g.add((crm.E52_Time_Span, rdfs.label , Literal('Time-Span')))
    """time-span for production event"""
    #medium
    medium_triple(row['mediumI'], row['cho_id'],'mediumI')
    medium_triple(row['mediumII'], row['cho_id'],'mediumII')
    medium_triple(row['mediumIII'], row['cho_id'],'mediumIII')
    medium_triple(row['mediumIV'], row['cho_id'],'mediumIV')
    medium_triple(row['mediumV'], row['cho_id'],'mediumV')
    medium_triple(row['mediumVII'], row['cho_id'],'mediumVII')
    medium_triple(row['mediumVIII'], row['cho_id'],'mediumVIII')
    #creationdate
    if row['cdate'] != 'nan':
        g.add((URIRef(ex+'timespan/'+'1/'+row['cho_id']), rdfs.label, Literal(row['cdate'])))
        """dates are not available in a coherent data format, rdfs.label is used until data cleaning"""
    #creator
    if Literal(row['intavia_id']) != 'nan':
        g.add((URIRef(ex+'production_event/'+row['cho_id']), bioc.had_participant_in_role, (URIRef(ex+'role/'+'responsibleArtist'+'/'+row['cho_id']))))
        """define participant as responsible artist in production event"""
        g.add((URIRef(ex+'personproxy/'+'europeana/'+row['intavia_id']), bioc.bearer_of, (URIRef(ex+'role/'+'responsibleArtist'+'/'+row['cho_id']))))
        """specific responsible person for CHO production event"""
        g.add((URIRef(ex+'role/'+'responsibleArtist'+'/'+row['cho_id']), RDF.type, bioc.Event_Role))
        g.add((bioc.Event_Role, rdfs.label , Literal('Event Role')))
        """define role as bioc actor role"""
        g.add((URIRef(idm+'role/'+'responsibleArtist'+'/'+row['cho_id']), rdfs.label, Literal('responsible Artist')))
        """human-readable label for type of role"""
    #title
    if (row['title']) != "nan":
        g.add((URIRef(ex+'choproxy/'+row['cho_id']), crm.P1_is_identified_by, (URIRef(ex+'cho/'+row['cho_id']+'/title'))))
        g.add(((URIRef(ex+'cho/'+row['cho_id']+'/title'), rdfs.label, Literal(row['title']))))
        g.add((URIRef(ex+'cho/'+row['cho_id']+'/title'), RDF.type, crm.E41_E33_Linguistic_Appellation))
        g.add((crm.E33_E41_Linguistic_Appellation , rdfs.label , Literal('Linguistic Appellation')))
        """adds title to CHO"""
    #description
    if (row['description']) != "nan":
            g.add((URIRef(ex+'role/'+'description/'+row['cho_id']), crm.P3_has_note, Literal(row['description'])))
            """adds description to CHO"""
    #relation
    if (row['relation']) != "nan":
        g.add((URIRef(ex+'choproxy/'+row['cho_id']), crm.P130_shows_features_of, (URIRef(row['relation']))))
        """relation to other CHO (edm: The name or identifier of a related resource, generally used for other related CHOs. The recommended best practice is to identify the resource using a formal identification scheme.)"""
    #extent
    if (row['extent']) != "nan":
        g.add((URIRef(ex+'measurementevent/'+row['cho_id']), crm.P39_measured, (URIRef(ex+'choproxy/'+row['cho_id']))))
        g.add((URIRef(ex+'measurementevent/'+row['cho_id']), RDF.type, crm.E16_Measurement))
        g.add((crm.E16_Measurement , rdfs.label , Literal('Measurement')))
        g.add((URIRef(ex+'measurementevent/'+row['cho_id']), crm.P40_observed_dimension, (URIRef(ex+'measurement/'+row['cho_id']))))
        g.add((URIRef(ex+'measurement/'+row['cho_id']), rdfs.value, Literal(row['extent'])))
        """a more detailed modeling (with measurement unit and type of measurement) is not possible until data is structured"""
    #dataProvider
    g.add((URIRef(ex+'choproxy/'+row['cho_id']), edm.dataProvider, Literal(row['dp'])))
    #modelling in Cidoc to be discussed
    #mediafiles, just images
    if (row['mf']) != "nan":
        g.add((URIRef(row['mf']), crm.P138_represents, (URIRef(ex+'choproxy/'+row['cho_id']))))
        g.add((URIRef(row['mf']), RDF.type, crm.E36_Visual_Item))
        g.add((URIRef(row['mf']), crm.P104_is_subject_to, (URIRef(row['rights']))))
        g.add((URIRef(row['rights']), RDF.type, crm.E30_Right))
        g.add((crm.E30_Right , rdfs.label , Literal('Right')))
    #general technique/ type
    type_triple(row['typeI'], row['cho_id'],'typeI')
    type_triple(row['typeII'], row['cho_id'],'typeII')
    type_triple(row['typeIII'], row['cho_id'],'typeIII')
    type_triple(row['typeIV'], row['cho_id'],'typeIV')
    type_triple(row['typeV'], row['cho_id'],'typeV')
    type_triple(row['typeVII'], row['cho_id'],'typeVII')
    type_triple(row['typeVIII'], row['cho_id'],'typeVIII')
    type_triple(row['typeIX'], row['cho_id'],'typeIX')
    type_triple(row['typeX'], row['cho_id'],'typeX')
    #subject
    subject_triple(row['subjectI'], row['cho_id'],'subjectI')
    subject_triple(row['subjectII'], row['cho_id'],'subjectII')
    subject_triple(row['subjectIII'], row['cho_id'],'subjectIII')
    subject_triple(row['subjectIV'], row['cho_id'],'subjectIV')
    subject_triple(row['subjectV'], row['cho_id'],'subjectV')

#labels for implemented classes
#g.add((crm.E16_Measurement , rdfs.label , Literal('Measurement')))



g.bind('crm', crm)
g.bind('ex', ex)
g.bind('ore', ore)
g.bind('edm', edm)
g.bind('owl', owl)
g.bind('rdf', rdf)
g.bind('xml', xml)
g.bind('xsd', xsd)
g.bind('bioc', bioc)
g.bind('rdfs', rdfs)
g.bind('apis', apis)
g.bind('idm', idm)
g.bind('owl', owl)
#Bind namespaces to prefixes for more readable output
 
 
exttl = g.serialize(format='turtle')    

with open('exdataset.rdf', 'w') as f:
    f.write(str(exttl))
"""Write graph data in file."""