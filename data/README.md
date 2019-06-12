### Layers

#### pz (shapes)
- Manually drawn line segments of varying lengths, each representing a length of curb with particular regulations
- shape: (3349, 18)
- GeoDataFrame (lines)
- column `GlobalID` is unique identifier

#### pza (images)
- Related table with links to photos of signs
- shape: (3162, 7)
- DataFrame
- column `GLOBALID` is unique identifier
- column `REL_GLOBALID` has 3130 unique values out of 3162 rows (32 duplicate values)
- `DATA` column has byte image

#### pzr (rules)
- Related table with a record for each unique regulation (many to one with Parking_Zones lines)
- shape: (4514, 19)
- DataFrame
- column `GlobalID` is unique identifier
- column `GUID` has 3203 unique values out of 4514 rows
- `GlobalID` and `GUID` never have the same value

### Relationships

#### `pz` (shapes) to `pza` (images)
- `pz['GlobalID']` joins to `pza['REL_GLOBALID']` linking shapes to images
    - **3130** of `pz['GlobaID']` (shapes UUID) are in `pza['REL_GLOBALID']` (image non-UUID) while **219** aren't
        - *i.e. not quite every shape has an image associated with it*
    - all **3162** values of `pz['REL_GLOBALID']` are in `pz['GlobalID']` 
        - *all images have a shape associated with them*
        - *there are **32** extra images that duplicates for individual street segments)*
    
#### `pz` (shapes) to `pzr` (rules)
- `pz['GlobalID']` joins to `pzr['GUID']`
    - **3203** values of `pz['GlobalID']` (shapes) are in `pza['GUID']` (rules non-UUID), **146** are not
        - *most but not all of the shapes have rules associated with them*
        - *every unique value of rules has a shape associated with it, every rule has a shape associated with it*
    - **4501** values of `pzr['GUID']` are in `pz['GlobalID']`, **13** are not
        - *I can't square this one. almost all of the non-unique ids of rules have a shape associates with them. but if the number of unique shapes matches the number of unique values in `pzr['GUID']` then how does every rule not have a shape associated with it.*

#### `pza` (images) to `pzr` (rules)
- `pza['REL_GLOBALID']` joins to `pzr['GUID']`
    - **4288** values of `pzr['GUID']` (non-unique rule identifiers) are in `pza['REL_GLOBALID']` (non-unique image identifiers), **226** are not
        - *most of the rules have images associated with them but there are more rules than images so there are many cases in which more than one rule is associated with an image*
        - *there are 226 rules that don't have images associated with them*
    - **3030** values of `pza['REL_GLOBALID']` (non-unique image identifiers) are in `pzr['GUID']` (non-unique rule identifiers), **132** are not
        - *most of the images images have rules associated with them. There are 132 images that just don't have any rules associated.*


### Objectives

- We are trying to create a data set at the street segment (i.e. *shapes*, *pz*) level 

