[![DOI](https://zenodo.org/badge/407187246.svg)](https://zenodo.org/badge/latestdoi/407187246)

# idm-rdf
## Intavia Data Model for RDF data
**IDM (InTaVia data model)** (in progress) combines *Cidoc CRM version 7.1.1* (https://cidoc-crm.org/rdfs/7.1.1/CIDOC_CRM_v7.1.1.rdfs), *BioCRM extension*, *EDM/ Europana Data Model* (based on EDM OWL, aligned with EDM version 5.2.4, last update: 2013-05-20 (to be replaced with version 5.2.8 manually or get current EDM OWL from Europeana), skos:definition of EDM is implemented as rdfs:comment), PROV-O and Open Archives Initiatives ORE (Version 1.0, 2008-10-17)).

## Entities
- The involvement of persons, groups and things (all subclasses of crm:E39 Actor) in events is modelled with bioCRM extension to allow typing of roles in events (with bioc:Event_Role, subclass of bioc:Entity_Role)
- bioc:Unary_Roles for persons are included to model the atemporal roles nationality, gender and occupation
- different bioc relationship roles for groups and persons are included (all subclasses of bioc:Entity_Role)
- IDM Proxies are proxies for Provided Entities, they are subclasses of ore:Proxy. The corresponding properties are subclasses of ore:proxyFor.
In IDM there are three kinds of Proxy classes and relations.

   | idm:CHO_Proxy | idm:cho_proxy_for | idm:ProvidedCHO
   | --- | --- | --- |  
   | idm:Group_Proxy | idm:group_proxy_for | idm:Provided_Group
   idm:Person_Proxy | idm:person_proxy_for | idm:Provided_Person

   This is an adapted interpretation of Europeana's proxy model, which adapts the OAI/ORE model.
- There are several Cidoc CRM events which are used to model metadata related to CHOs: crm:E10 Transfer of Custody, crm:E11 Modification (create, alter or change CHOs), crm:E12 Production (Production of CHOs), E15 Identifier Assignment (to assign E42 Identifiers), E16 Measurement, E6 Destruction, E8 Acquisition, E9 Move, 
CHO_Proxies may be added or removed from crm:E78 Curated Holding (Typical instances of curated holdings are museum collections, archives, library holdings and digital libraries)
- crm:E42 Identifier does not apply to URIs (we use owl:sameAs to avoid confusion) but to any other Identifier which has been assigned to a CHO_Proxy
the new merged E41_E33_Linguistic_Appellation class from Cidoc CRMs RDF implementation for version 7.1.1, defined as subClassOf `E41 Appellation` and `E33 Linguistic Object`, for all Appellations being regarded specific to or characteristic for a language group and being described indirectly via a URI was added to IDM. It allows to assign languages to appellation which is especially important for Cultural Heritage and Groups (partly also useful for person names)
- all data properties have the range rdfs:literal (according to https://cidoc-crm.org/rdfs/7.1.1/CIDOC_CRM_v7.1.1.rdfs)
- the entity edm:dataProvider and its properties are adapted to keep the information in the dataset in an unambiguous form.

## Object Properties
- in IDM “idm:CHO_Proxy crm:P3_has_note rdfs:Literal” is equivalent to the edm use of dc:description (A description of the original analog or born digital object, title or description is mandatory in Europeana)
- inscriptions in CHOs are modelled as “idm:CHO_Proxy crm:P128_carries crm:E33 Linguistic_Object crm:P3_has_note rdfs:Literal”
- Appellations for persons are modelled with name components and typing with the properties crm:P148_has_component and crm:P2_has_type
- additional information to events (Creation, Modification, Destruction, Move etc) can be added with the properties crm:P15 was influenced by, P17 was motivated by
- additional information can be added to CHOs with the properties: P19 was intended use of (for items that were created for a specific event), P32 used general technique, P45 consists of (range: E57 Material), P62_depicts
- crm:P2 has type property can be appended to the classes: crm:E11_Modification , crm:E41_Appellation, crm:E42_Identifier, crm:E54_Dimension and edm:ProvidedCHO

## Data Properties
- according to the Cidoc CRM 7.1.1 RDFS specification (https://cidoc-crm.org/rdfs/7.1.1/CIDOC_CRM_v7.1.1.rdfs ), all ranges of the included data properties (properties which have the range of E59 Primitive or subclasses of E59 Primitive) have the range rdfs:Literal (applied for ranges of properties: P168 place is defined by, P3 has note, P102 has title, P90 has value)
