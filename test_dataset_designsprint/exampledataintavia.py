#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 09:58:52 2020

@author: CE
"""

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

pldf.columns = ['intavia_id', 'forename', 'surname', 'birthdate', 'birthplace', 'deathdate', 'deathplace', 'occupation_general', 'gender', 'nationality','sibling_forename','sibling_surname', 'apis_id']

chodf.columns = ['cho_id','person_id','item','title','coverage','created','description','relation','subject','type']



pldf = pldf.applymap(str)
"""Convert all items in the Personlistdataframe to strings."""
chodf = chodf.applymap(str)


g = Graph()
#Create undirected graph, assigned to g 
 
for index, row in pldf.iterrows():
    """Create RDF Triples, according to IDM ontology."""
    g.add((URIRef(ex+'person/'+row['intavia_id']), RDF.type, idm.Provided_Person))
    """Initialize URI for E21 Person"""
    g.add((URIRef(ex+'personproxy/'+row['intavia_id']), idm.person_proxy_for, URIRef(ex+'person/'+row['intavia_id'])))
    """add person proxy to person"""
    g.add((URIRef(ex+'personproxy/'+row['intavia_id']), RDF.type, idm.Person_Proxy))
    g.add((URIRef(ex+'personproxy/'+row['intavia_id']), RDF.type, crm.E21_Person))
    """declare Person_Proxy"""
    g.add((URIRef(ex+'personproxy/'+row['intavia_id']), crm.P1_is_identified_by, (URIRef(apis+'personid/'+row['apis_id']))))
    """Add APIS Identifier for Statement to Person Proxy"""
    g.add((URIRef(ex+'personid/'+row['apis_id']), RDF.type, crm.E42_Identifier))
    """define APIS ID as Identifier"""
    g.add((URIRef(ex+'personid/'+row['apis_id']), crm.P3_has_note , (Literal(row['apis_id']))))
    """add value of APIS ID"""
    g.add((URIRef(ex+'personid/'+row['apis_id']), crm.P2_has_type, (Literal('APIS Identifier'))))
    """define type of Identifier"""
    g.add((URIRef(ex+'identassig/'+row['intavia_id']), RDF.type, crm.E15_Identifier_Assignment))
    """defined event as Identifier Assignment"""
    g.add((URIRef(ex+'identassig/'+row['intavia_id']), crm.P37_assigned, (URIRef(apis+'personid/'+row['apis_id']))))
    """Identifier Assignment assigned Identifier"""
    g.add((URIRef(ex+'identassig/'+row['intavia_id']), bioc.had_participant_in_role, (URIRef(ex+'role/'+'ResponsibleForIdentifier'+'/'+row['intavia_id']))))
    """Identifier Assignment had participant in role ResponsibleForIdentifier"""
    g.add((URIRef(ex+'role/'+'ResponsibleForIdentifier'+'/'+row['intavia_id']), RDF.type, bioc.Event_Role))
    """assigned role as an actor role"""
    g.add((URIRef(ex+'institution/'+'AustrianAcademyofSciences'), bioc.bearer_of, (URIRef(idm+'role/'+'ResponsibleForIdentifier'+'/'+row['intavia_id']))))
    """defines who is responsible for the identifier assignment"""
    g.add((URIRef(idm+'role/'+'ResponsibleForIdentifier'+'/'+row['intavia_id']), crm.P2_has_type, Literal('ResponsibleForIdentifier')))
    """defines type of role"""
    #name
    g.add((URIRef(ex+'personproxy/'+row['intavia_id']), crm.P1_is_identified_by, (URIRef(ex+'name/'+'1/'+row['intavia_id']))))
    """add name to Person Proxy"""
    g.add((URIRef(ex+'name/'+'1/'+row['intavia_id']), RDF.type, crm.E41_Appellation))
    """defines name as Cidoc E41 Appellation"""
    g.add((URIRef(ex+'name/'+'1/'+row['intavia_id']), crm.P148_has_component, (URIRef(ex+'name/'+'2/'+row['intavia_id']))))
    """add surname"""
    g.add((URIRef(ex+'name/'+'2/'+row['intavia_id']), crm.P2_has_type, Literal("surname")))
    """define as type surname"""
    g.add((URIRef(ex+'name/'+'2/'+row['intavia_id']), crm.P3_has_note , (Literal(row['surname']))))
    """add string for surname"""
    g.add((URIRef(ex+'name/'+'1/'+row['intavia_id']), crm.P148_has_component, (URIRef(ex+'name/'+'3/'+row['intavia_id']))))
    """add forename"""
    g.add((URIRef(ex+'name/'+'3/'+row['intavia_id']), crm.P2_has_type , Literal("forename")))
    """define as type forename"""
    g.add((URIRef(ex+'name/'+'3/'+row['intavia_id']), crm.P3_has_note , (Literal(row['forename']))))
    """add string for forename"""
    g.add((URIRef(ex+'birthevent/'+row['intavia_id']), crm.P98_brought_into_life, (URIRef(ex+'personproxy/'+row['intavia_id']))))
    """adds birth event to Person Proxy"""
    g.add((URIRef(ex+'birthevent/'+row['intavia_id']), RDF.type, crm.E67_Birth))
    """"defines event as Cidoc Birth Event"""
    g.add((URIRef(ex+'birthevent/'+row['intavia_id']), crm.P4_has_time_span, (URIRef(ex+'timespan/'+'1/'+row['intavia_id']))))
    """time span for birth event"""
    g.add((URIRef(ex+'timespan/'+'1/'+row['intavia_id']), RDF.type, crm.E52_Time_Span))
    g.add((URIRef(ex+'timespan/'+'1/'+row['intavia_id']), crm.P81a_begin_of_the_begin, (Literal(row['birthdate'])+'+00:00:00')))
    """defines begin of birthdate"""
    g.add((URIRef(ex+'timespan/'+'1/'+row['intavia_id']), crm.P82b_end_of_the_end, (Literal(row['birthdate'])+'+23:59:59')))
    """defines begin of birthdate"""
    g.add((URIRef(ex+'deathevent/'+row['intavia_id']), crm.P100_was_death_of, (URIRef(ex+'personproxy/'+row['intavia_id']))))
    """adds death event to Person Proxy"""
    g.add((URIRef(ex+'deathevent/'+row['intavia_id']), RDF.type, crm.E69_Death))
    g.add((URIRef(ex+'deathevent/'+row['intavia_id']), RDF.type, crm.E5_Event))
    """"defines event as Cidoc Birth Event"""
    g.add((URIRef(ex+'deathevent/'+row['intavia_id']), crm.P4_has_time_span, (URIRef(ex+'timespan/'+'2/'+row['intavia_id']))))
    """time span for death event"""
    g.add((URIRef(ex+'timespan/'+'2/'+row['intavia_id']), crm.P81a_begin_of_the_begin, (Literal(row['deathdate'])+'+00:00:00')))
    """defines begin of deathdate"""
    g.add((URIRef(ex+'timespan/'+'2/'+row['intavia_id']), RDF.type, crm.E52_Time_Span))
    g.add((URIRef(ex+'timespan/'+'2/'+row['intavia_id']), crm.P82b_end_of_the_end, (Literal(row['deathdate'])+'+23:59:59')))
    """defines end of deathdate"""
    g.add((URIRef(ex+'personproxy/'+row['intavia_id']), bioc.has_gender, (URIRef(bioc+row['gender']))))
    g.add((URIRef(bioc+row['gender']), RDF.type, bioc.Gender))
    """define Gender as biocrm gender"""
    g.add((URIRef(ex+'personproxy/'+row['intavia_id']), bioc.has_occupation, (URIRef(bioc+row['occupation_general']))))
    """add occupation to Person Proxy"""
    g.add((URIRef(bioc+row['occupation_general']), RDF.type, bioc.Occupation))
    """define occupation as biocrm occupation"""
    g.add((URIRef(ex+'personproxy/'+row['intavia_id']), bioc.has_nationality, (URIRef(bioc+row['nationality']))))
    """add nationality to Person Proxy"""
    g.add((URIRef(bioc+row['nationality']), RDF.type, bioc.Nationality))
    """define nationality as biocrm nationality"""
    if (row['sibling_surname']) != "nan":
        g.add((URIRef(ex+'personproxy/'+row['intavia_id']), bioc.has_family_relation, (URIRef(ex+'familyrelation/'+'1/'+row['intavia_id']))))
        """add family relation"""
        g.add((URIRef(ex+'familyrelation/'+'1/'+'/'+row['intavia_id']), RDF.type, bioc.Family_Relation))
        """family relation is from Bioc"""
        g.add((URIRef(ex+'familyrelation/'+'1/'+'/'+row['intavia_id']), crm.P2_has_type, Literal('Sibling')))
        """add type of relation"""
        g.add((URIRef(ex+'familyrelation/'+'1/'+'/'+row['intavia_id']), bioc.inheres_in, (URIRef(ex+'personproxy/'+row['sibling_forename']+row['sibling_surname']))))
        """points to second person in family relation"""
        g.add((URIRef(ex+'person/'+row['sibling_forename']+row['sibling_surname']), RDF.type, idm.Provided_Person))
        g.add((URIRef(ex+'personproxy/'+row['sibling_forename']+row['sibling_surname']), RDF.type, idm.Person_Proxy))
        g.add((URIRef(ex+'personproxy/'+row['sibling_forename']+row['sibling_surname']), idm.person_proxy_for, (URIRef(ex+'person/'+row['sibling_forename']+row['sibling_surname']))))
        g.add((URIRef(ex+'personproxy/'+row['sibling_forename']+row['sibling_surname']), RDF.type, crm.E21_Person))
        """defines sibling as person"""
        g.add((URIRef(ex+'personproxy/'+row['sibling_forename']+row['sibling_surname']), crm.P1_is_identified_by, (URIRef(ex+'name/'+'1/'+row['sibling_forename']+row['sibling_surname']))))
        """add name to Person Proxy"""
        g.add((URIRef(ex+'name/'+'1/'+row['sibling_forename']+row['sibling_surname']), RDF.type, crm.E41_Appellation))
        """defines name as Cidoc E41 Appellation"""
        g.add((URIRef(ex+'name/'+'1/'+row['sibling_forename']+row['sibling_surname']), crm.P148_has_component, (URIRef(ex+'name/'+'2/'+row['sibling_forename']+row['sibling_surname']))))
        """add surname"""
        g.add((URIRef(ex+'name/'+'2/'+row['sibling_forename']+row['sibling_surname']), RDF.type, crm.E41_Appellation))
        """defines surname as Cidoc E41 Appellation"""
        g.add((URIRef(ex+'name/'+'2/'+row['sibling_forename']+row['sibling_surname']), crm.P2_has_type, Literal('surname')))
        """define as type surname"""
        g.add((URIRef(ex+'name/'+'2/'+row['sibling_forename']+row['sibling_surname']), crm.P3_has_note , (Literal(row['sibling_surname']))))
        """add string for surname"""
        g.add((URIRef(ex+'name/'+'1/'+row['sibling_forename']+row['sibling_surname']), crm.P148_has_component, (URIRef(ex+'name/'+'3/'+row['sibling_forename']+row['sibling_surname']))))
        """add forename"""
        g.add((URIRef(ex+'name/'+'3/'+row['sibling_forename']+row['sibling_surname']), RDF.type, crm.E41_Appellation))
        """defines forename as Cidoc E41 Appellation"""
        g.add((URIRef(ex+'name/'+'3/'+row['sibling_forename']+row['sibling_surname']), crm.P2_has_type, Literal('forename')))
        """define as type forename"""
        g.add((URIRef(ex+'name/'+'3/'+row['sibling_forename']+row['sibling_surname']), crm.P3_has_note , (Literal(row['sibling_forename']))))
        """add string for forename"""

for index, row in chodf.iterrows():
    g.add((URIRef(ex+'production_event/'+row['cho_id']), RDF.type, crm.E12_Production))
    g.add((URIRef(ex+'production_event/'+row['cho_id']), RDF.type, crm.E5_Event))
    """define production event"""
    g.add((URIRef(ex+'cho/'+row['cho_id']), RDF.type, idm.Provided_CHO))
    g.add((URIRef(ex+'choproxy/'+row['cho_id']), idm.cho_proxy_for, (URIRef(ex+'cho/'+row['cho_id']))))
    g.add((URIRef(ex+'choproxy/'+row['cho_id']), RDF.type, idm.CHO_Proxy))
    if Literal(row['person_id']) != "nan":
        g.add((URIRef(ex+'production_event/'+row['cho_id']), bioc.had_participant_in_role, (URIRef(ex+'role/'+'responsibleArtist'+'/'+row['cho_id']))))
        """define participant in production event"""
        g.add((URIRef(ex+'personproxy/'+row['person_id']), bioc.bearer_of, (URIRef(ex+'role/'+'responsibleArtist'+'/'+row['cho_id']))))
        """defines who is responsible for the artwork"""
        g.add((URIRef(ex+'role/'+'responsibleArtist'+'/'+row['cho_id']), RDF.type, bioc.Event_Role))
        """define role as bioc actor role"""
        g.add((URIRef(idm+'role/'+'responsibleArtist'+'/'+row['cho_id']), crm.P2_has_type, Literal('responsibleArtist')))
        """defines type of role"""
    if (row['title']) != "nan":
        g.add((URIRef(ex+'choproxy/'+row['cho_id']), crm.P1_is_identified_by, (URIRef(ex+'cho/'+'title/'+row['cho_id']))))
        g.add(((URIRef(ex+'cho/'+'title/'+row['cho_id']), crm.P3_has_note,Literal(row['title']))))
        """adds title to CHO"""
    if (row['description']) != "nan":
            g.add((URIRef(ex+'role/'+'description/'+row['cho_id']), crm.P3_has_note, Literal(row['description'])))
            """adds description to CHO"""
    if (row['relation']) != "nan":
        g.add((URIRef(ex+'choproxy/'+row['cho_id']), crm.P130_shows_features_of, (URIRef(row['relation']))))
        """relation to other CHO (edm: The name or identifier of a related resource, generally used for other related CHOs. The recommended best practice is to identify the resource using a formal identification scheme.)"""
    #g.add((URIRef(ex+'production_event/'+row['cho_id']), crm.P7_took_place_at, Literal(row['coverage'])))
    #"""adds region to CHO (edm category includes also temporal contextualisation, but these links don't work, we have to seperate these values in the data ingestion pipeline, regions are geonames references, temporal contextualisation is from semium.org (e.g. https://semium.org/time/1979))"""
    #not 100% accurate for this concrete cidoc Event
    #g.add((URIRef(ex+'rights/'+row['cho_id']), crm.P129_is_about, (URIRef(ex+'cho/'+row['cho_id']))))
    #"""Rights on the DIGITAL object, not the actual CHO"""
    #g.add((URIRef(ex+'rights/'+row['cho_id']), RDF.type, crm.E30_Right)
    #"""defines those rights as E30 rights"""
    #g.add(row['rights'], crm.P75_possesses, (URIRef(ex+'rights/'+row['cho_id']))



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
 
exttl = g.serialize(format='turtle').decode('utf-8')    

with open('exdataset.rdf', 'w') as f:
    f.write(str(exttl))
"""Write graph data in file."""
