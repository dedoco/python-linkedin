import datetime

from xml.dom import minidom
from xml.sax.saxutils import unescape

def get_child(node, tagName):
    try:
        domNode = node.getElementsByTagName(tagName)[0]
        childNodes = domNode.childNodes
        if childNodes:
            return childNodes[0].nodeValue
        return None
    except:
        return None

def parse_connections(connections_node):
    connections_list = []
    connections = connections_node.getElementsByTagName("connection")
    if connections:
        for connection in connections:
            person = connection.getElementsByTagName("person")
            if person:
                person = person[0]
                connections_list.append(Profile.create(person))

    return connections_list

class LinkedInModel:
    
    def __repr__(self):
        d = {}
        for x,y in self.__dict__.items():
            if (self.__dict__[x]):
                d[x] = y
        return (self.__module__ + "." + self.__class__.__name__ + " " +
                d.__repr__())
        
    
class Education(LinkedInModel):
    """
    Class that wraps an education info of a user
    """
    def __init__(self):
        self.id          = None
        self.school_name = None
        self.degree      = None
        self.start_date  = None
        self.end_date    = None
        self.activities  = None
        self.notes       = None
        self.field_of_study = None
        
    @staticmethod
    def create(node):
        """
        <educations total="">
         <education>
          <id>
          <school-name>
          <degree>
          <start-date>
           <year>
          </start-date>
          <end-date>
           <year>
          </end-date>
         </education>
        </educations>
        """
        children = node.getElementsByTagName("education")
        result = []
        for child in children:
            education = Education()
            education.id = education._get_child(child, "id")
            education.activities = education._get_child(child, "activities")
            education.notes = education._get_child(child, "notes")
            education.school_name = education._get_child(child, "school-name")
            education.degree = education._get_child(child, "degree")
            education.field_of_study = education._get_child(child, "field-of-study")
            start_date = child.getElementsByTagName("start-date")
            if start_date:
                start_date = start_date[0]
                try:
                    year = int(education._get_child(start_date, "year"))
                    education.start_date = datetime.date(year, 1, 1)
                    month = int(education._get_child(start_date, "month"))
                    education.start_date = datetime.date(year, month, 1)
                except Exception:
                    pass

            end_date = child.getElementsByTagName("end-date")
            if end_date:
                end_date = end_date[0]
                try:
                    year = int(education._get_child(end_date, "year"))
                    education.end_date = datetime.date(year, 1, 1)
                    month = int(education._get_child(end_date, "month"))
                    education.end_date = datetime.date(year, month, 1)
                except Exception:
                    pass

            result.append(education)            
        return result
    
    def _get_child(self, node, tagName):
        try:
            domNode = node.getElementsByTagName(tagName)[0]
            childNodes = domNode.childNodes
            if childNodes:
                return childNodes[0].nodeValue
            return None
        except:
            return None

class Position(LinkedInModel):
    """
    Class that wraps a business position info of a user
    """
    def __init__(self):
        self.id         = None
        self.title      = None
        self.summary    = None
        self.start_date = None
        self.end_date   = None
        self.company    = None
        

    @staticmethod
    def create(node):
        """
        <positions total='1'>
         <position>
          <id>101526695</id>
          <title>Developer</title>
          <summary></summary>
          <start-date>
          <year>2009</year>
          <month>9</month>
          </start-date>
          <is-current>true</is-current>
          <company>
          <name>Akinon</name>
          </company>
         </position>
        </positions>
        """
        children = node.getElementsByTagName("position")
        result = []
        for child in children:
            position = Position()
            position.id = get_child(child, "id")
            position.title = get_child(child, "title")
            position.summary = get_child(child, "summary")
            company = child.getElementsByTagName("company")
            if company:
                company = company[0]
                position.company = get_child(company, "name")
            
            start_date = child.getElementsByTagName("start-date")
            if start_date:
                start_date = start_date[0]
                try:
                    year = int(get_child(start_date, "year"))
                    position.start_date = datetime.date(year, 1, 1)
                    month = int(get_child(start_date, "month"))
                    position.start_date = datetime.date(year, month, 1)
                except Exception:
                    pass

            end_date = child.getElementsByTagName("end-date")
            if end_date:
                end_date = end_date[0]
                try:
                    year = int(get_child(end_date, "year"))
                    position.end_date = datetime.date(year, 1, 1)
                    month = int(get_child(end_date, "month"))
                    position.end_date = datetime.date(year, month, 1)
                except Exception:
                    pass

            result.append(position)

        return result
        
class Location(LinkedInModel):
    def __init__(self):
        self.name = None
        self.country_code = None
        
    @staticmethod
    def create(node):
        """
        <location>
            <name>
            <country>
                <code>
            </country>
        </location>
        """
        loc = Location()
        loc.name = get_child(node, "name")
        country = node.getElementsByTagName("country")
        if country:
            country = country[0]
            loc.country_code = get_child(country, "code")
            
        return loc
    
class RelationToViewer(LinkedInModel):
    def __init__(self):
        self.distance = None
        self.num_related_connections = None
        self.connections = []
        
    @classmethod
    def create(cls, node):
        """
        <relation-to-viewer>
            <distance>1</distance>
            <connections total="36" count="10" start="0">
                <connection>
                    <person>
                        <id>_tQbzI5kEk</id>
                        <first-name>Michael</first-name>
                        <last-name>Green</last-name>
                    </person>
                </connection>
            </connections>
        </relation-to-viewer>
        """
        relation = RelationToViewer()
        relation.distance = int(get_child(node, "distance"))
        relation.num_related_connections = int(get_child(node, "num-related-connections"))
        
        connections = node.getElementsByTagName("connections")
        if connections:
            connections = connections[0]
            if not relation.num_related_connections:
                if connections.hasAttribute("total"):
                    relation.num_related_connections = int(connections.attributes["total"].value)

            relation.connections = parse_connections(connections)
                    
        return relation
    
class Profile(LinkedInModel):
    """
    Wraps the data which comes from Profile API of LinkedIn.
    For further information, take a look at LinkedIn Profile API.
    """
    def __init__(self):
        self.id          = None
        self.first_name  = None
        self.last_name   = None
        self.headline    = None
        self.location    = None
        self.industry    = None
        self.distance    = None
        self.relation_to_viewer = None
        self.summary     = None
        self.specialties = None
        self.interests   = None
        self.honors      = None
        self.public_url  = None
        self.private_url = None
        self.picture_url = None
        self.current_status = None
        self.current_share = None
        self.languages   = []
        self.skills      = []
        self.connections = []
        self.positions   = []
        self.educations  = []
        self.xml_string  = None
        
    @staticmethod
    def create(node, debug=False):
        try:
            person = node
            if person.nodeName != "person":
                person = person.getElementsByTagName("person")[0]
            profile = Profile()
            profile.id = get_child(person, "id")
            profile.first_name = get_child(person, "first-name")
            profile.last_name = get_child(person, "last-name")
            profile.headline = get_child(person, "headline")
            profile.distance = get_child(person, "distance")
            profile.specialties = get_child(person, "specialties")
            profile.industry = get_child(person, "industry")
            profile.honors = get_child(person, "honors")
            profile.interests = get_child(person, "interests")
            profile.summary = get_child(person, "summary")
            profile.picture_url = profile._unescape(get_child(person, "picture-url"))
            profile.current_status = get_child(person, "current-status")
            profile.current_share = get_child(person, "current-share")
            profile.public_url = profile._unescape(get_child(person, "public-profile-url"))

            location = person.getElementsByTagName("location")
            if location:
                profile.location = Location.create(location[0])

            relation_to_viewer = person.getElementsByTagName("relation-to-viewer")
            if relation_to_viewer:
                relation_to_viewer = relation_to_viewer[0]
                profile.relation_to_viewer = RelationToViewer.create(relation_to_viewer)

            connections = person.getElementsByTagName("connections")
            if connections:
                connections = connections[0]
                profile.connections = parse_connections(connections)

            # TODO Last field working on is - num_connections

            private_profile = person.getElementsByTagName("site-standard-profile-request")
            if private_profile:
                private_profile = private_profile[0]
                profile.private_url = get_child(private_profile, "url")

            # create skills
            skills = person.getElementsByTagName("skills")
            if skills:
                skills = skills[0]
                children = skills.getElementsByTagName('skill')
                for child in children:
                    if not child.getElementsByTagName('id'):
                        profile.skills.append(get_child(child, 'name'))

            # create languages
            languages = person.getElementsByTagName("languages")
            if languages:
                languages = languages[0]
                children = languages.getElementsByTagName('language')
                for child in children:
                    if not child.getElementsByTagName('id'):
                        profile.languages.append(get_child(child, 'name'))

            # create positions
            positions = person.getElementsByTagName("positions")
            if positions:
                positions = positions[0]
                profile.positions = Position.create(positions)

            # create educations
            educations = person.getElementsByTagName("educations")
            if educations:
                educations = educations[0]
                profile.educations = Education.create(educations)

            # For debugging
            if debug:
                profile.xml_string = node.toxml()

            return profile
        except:
            print "blat"
            return None
        """
        @This method is a static method so it shouldn't be called from an instance.

        Parses the given xml string and results in a Profile instance.
        If the given instance is not valid, this method returns NULL.
        """

        return None

    def _unescape(self, url):
        if url:
            return unescape(url)
        return url

    def _get_child(self, node, tagName):
        try:
            if tagName == "summary":
                for n in node.getElementsByTagName(tagName):
                    if n.parentNode.tagName == node.tagName:
                        domNode = n
                        break
            else:
                domNode = node.getElementsByTagName(tagName)[0]

            if domNode.parentNode.tagName == node.tagName:
                childNodes = domNode.childNodes
                if childNodes:
                    return childNodes[0].nodeValue
                return None
            else:
                return None
        except:
            return None