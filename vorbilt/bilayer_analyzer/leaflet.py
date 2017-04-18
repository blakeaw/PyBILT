


# leaflet object    
class Leaflet:
    """ Create a bilayer Leaflet representation.   
    This class object is used to group lipids together according to their bilayer leaflet. It is primarily meant to 
    store the indices of LipidCOMs as they are in a Frame.lipidcom list. This class also 
    creates sub-groups within the Leaflet based on the LipidCOM.type using LipidGroup objects. Instances of Leaflet
    are created by the MemSys class.
                
    """
    def __init__(self, name):
        """Initializes an instance of a Leaflet object.    
        
        Args:
            name (str): The name of the bilayer leaflet being initialized ('upper' and 'lower' are used by the MemSys class).
        
        Attributes:
            name (str): The name of the Leaflet (e.g. 'upper' or 'lower').
            members (list of int): A list containing the integer indices associated with the LipidCOM objects within
                a Frame that are assigned to the Leaflet instance.
            groups (list of obj:LipidGroup): A list of the LipidGroup objects (uniquely named) that are created by the Leaflet instance
                as new members are added.
            group_dict (dict): A dictionary keyed according to the names of the LipidGroup objects created, which stores the 
                corresponding index of that LipidGroup in self.groups. 
  
        """
        #the name of the leaflet - e.g. 'upper' or 'lower'
        self.name = name
        #initialize a list to store the indices of lipids assigned to this leaflet
        self.members = []
        #initialize a list to hold the LipidGroup objects 
        self.groups = []
        #initialize a dictionary to store the self.groups index of LipidGroup objects
        self.group_dict = {}
        return

    def __str__(self):
        return '%s leaflet of a Membrane System with %s members and %s lipid groups' % (self.name, len(self.members), len(self.groups)) 

    def __repr__(self):
        return '%s leaflet of a Membrane System with %s members and %s lipid groups' % (self.name, len(self.members), len(self.groups))
 
    def __len__(self):
        """ Have len(Leaflet) return the number of lipids that have been added to the Leaflet instance.
        
        Returns:
            int: Number of lipids in the Leaflet.
        """
        return len(self.members)

    #consider changing var name of input 'resname' to something that doesn't conflict with LipidCOM.type  
    def add_member(self, index, resname):
        """ Add new lipids to the Leaflet.
           
        This function is meant to be used to add new lipids according to their Frame.lipidcom index
        to the Leaflet and to a LipidGroup according resname/type/name. 
        Args:  
            index (int): The index of the lipid being added to the Leaflet.
            resname (str): The resname (or LipidCOM.type) of the lipid being added.
        """
        if len(self.members) == 0:
            self.members.append([index, resname])
            self.groups.append(LipidGroup(resname))
            self.groups[0].add_member(index)
            self.group_dict.update({resname: 0})
        else:
            self.members.append([index, resname])
            addgroup = True
            group_ind = 0
            for rn in self.groups:
                if resname == rn.lg_name:
                    addgroup = False
                    break
                group_ind+=1
            if addgroup:
                self.groups.append(LipidGroup(resname))
                ng = len(self.groups)
                self.groups[ng-1].add_member(index)
                self.group_dict.update({resname: ng-1})
            else:
                self.groups[group_ind].add_member(index)
            
            #self.members=sorted(self.members,key=lambda self.members:self.members[1])  
        return

    def get_group_indices(self, group_name):
        """ Get the indices of lipids in the Leaflet belonging to a specific LipidGroup.   

        Args:
        group_name (string): The name of the LipidGroup pull LipidCOM indices from. 
            Passing the string 'all' will return indices of all the lipids assigned to
            the Leaflet instance. If the group_name is not recognised (i.e. is not in the group_dict)
            The function defaults to 'all'.
                       
        Returns:
            list of int: A list containing the integer indices of lipids in the Leaflet that
                belong to the specified LipidGroup.
        """
        indices = []
        if group_name == "all":
            for element in self.group_dict:
                gindex = self.group_dict[element]
                indices += self.groups[gindex].lg_members
        elif group_name in self.group_dict:
            gindex = self.group_dict[group_name]
            indices = self.groups[gindex].lg_members
        else:
            #unkwown group name- print warning and use the default "all"
            print "!! Warning - request for unknown Lipid Group \'",group_name,"\' from the ",self.name," leaflet"
            print "!! using the default \"all\""
            for element in self.group_dict:
                gindex = self.group_dict[element]
                indices += self.groups[gindex].lg_members

        return list(indices)

    def get_member_indices(self):
        """ Get the indices of all lipids (LipidCOM) in the Leaflet.   
        This member function Returns: the list of indices for the lipids grouped in the Leaflet instance.
                           
        Returns:
            list of int: A list of integer indices of the lipids associated with the Leaflet instance.
        """
        indices = []
        for element in self.members:
            indices.append(element[0])

        return list(indices)

    def has_group(self, group_name):
        """ Check if there is a LipidGroup with the specified name.  
            
        Args:
            group_name (str): The name to checked against the names of existing LipidGroup objects.
                           
        Returns:
            bool: True if there is a LipidGroup with name group_name, and False otherwise.
        """
        return group_name in self.group_dict.keys()

    def num_groups(self):
        """ Get the number of LipidGroups in the Leaflet.   
    
        Returns:
        int: The number of unique LipidGroups.
        """
        return len(self.groups)

    def get_group_names(self):
        """ Get the names of all the LipidGroup objects in the Leaflet  

        Returns:
        list of str: A list of the names of current LipidGroup objects.
        """
        return [group.lg_name for group in self.groups]

        
class LipidGroup:
    """ Object to group lipid indices by type/resname/name.   
        Instances of this object are created by the Leaflet class.
                       
    """
    def __init__(self, name):
        """ Initializes LipidGroup object.               

        Args:
            name (str): The name/type/resname of the lipids being grouped in this object. 

        Attributes:
            lg_members (list of int): A list to hold the indices of lipids added to this 
                this LipidGroup.
            lg_name (str): The name/type/resname of the lipids being grouped in this object.
        """
        #initialize a list to hold the member indices
        self.lg_members = []
        # the name of this lipid group
        self.lg_name = name
        return

    def add_member(self, new_mem):
        """ Add lipid index to to the LipidGroup.
   
         Args:
            new_mem (int): The index of the lipid being added to this LipidGroup. 
        """
        self.lg_members.append(new_mem)
        return

    def name(self):
        """ Get the name associated with this LipidGroup.   

        Returns:               
            str: The name of the lipid group (i.e. lg_name) 
        """
        return self.lg_name