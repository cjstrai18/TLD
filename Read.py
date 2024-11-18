#encodes the characteristics of a singular TLD
class TLD: 
    def __init__(self, indx, nC, cf, pmt, ref): 
        self.info = {'number': indx, 'responses':[nC], 'chip_factors': [cf],
                     'PMT': [pmt], 'refrence_light': [ref], 'nC_mean' : 0, 
                    'nC_pct_SD' : 0, 'CF_mean' : 0, 'CF_pct_SD' : 0,}
    
    
    def add_read(self, response, chip_factor, PMT, refrence_light): 
        info_name = ['responses', 'chip_factors', 'PMT', 'refrence_light']
        info = [response, chip_factor, PMT, refrence_light]
        for val_name, val in zip(info_name, info): 
            self.info[val_name].append(val) 

#encodes the characteristics of a singular read via storing multiple tld objects
class Comparison: 
    
    def __init__(self, nC_paths, names, types = ['Chip']): 
        self.read_names = names
        self.num_groups = len(types) 
        self.types = types
        self.TLDs = []
        self.Reads = pd.DataFrame()
        for i,nC_path in enumerate(nC_paths): 
            self.pro_data(nC_path, names[i], i+1)
        self.comp_stats()
        self.Reads.index = range(1, self.Reads.shape[0]+ 1)
    
            
    def pro_data(self, path, name, read_num):              #processes file given path, creates/adds to tld objects
        read_nc = []
        read_cf = []
        PMT_Ref = []
        ttt = 0

        with open(path, 'r') as f: 
            readouts = f.readlines()                                   # Get entire file as list of strings 
            for readout in readouts:                                   # Iterate over each readout
                parsed_readout = readout.split(',')                    # Split into cols 
                if len(parsed_readout[2].replace(' ','')[1:-1]) <= 2:  # Check for pmt / ref entry 
                    read_nc.append(float(parsed_readout[-2].strip()))
                else: 
                    PMT_Ref.append(float(parsed_readout[-2].strip()))
                                     
        #storage of data on the read basis(only nC for now):
        gsize = int(len(read_nc) / self.num_groups)                   #if have mult TLD types, calcs CF for each 
        types = [item for item in self.types for _ in range(gsize)]   #labeling what type is in dataframe
        indx = 0                                                      #type individually 
        
        for i in range(self.num_groups): 
            read_cf += self.chip_factors(read_nc[indx:indx+gsize])
            indx+=gsize
        self.Reads['TLD Type'] = types
        self.Reads[f'{name} nC'] = read_nc
        self.Reads[f'{name} CF'] = read_cf
        
        for i, nc_cf in enumerate(zip(read_nc, read_cf)):              #create list of TLD objects,data on TLD basis
            nc = nc_cf[0]
            cf = nc_cf[1]
            if (i % 50 == 0) and (i != 0):                             #indexed st correct PMT, ref assigned
                ttt += 2 
            if read_num == 1:                                          
                tld = TLD(i+1, nc, cf, PMT_Ref[ttt], PMT_Ref[ttt+1])   
                self.TLDs.append(tld)
            else: 
                self.TLDs[i].add_read(nc, cf, PMT_Ref[ttt], PMT_Ref[ttt+1])
    
    
    def chip_factors(self, nc):                                        #returns list of chip factors
        cf = [] 
        median = statistics.median(nc) 
        for tld in nc: 
            cf.append(tld/median)
        return cf
    
    
    def highlight_row(self, row):
        if row['%SD CF'] > 3:
            return ['background-color: red']*len(row)
        else:
            return ['']*len(row)

    
    def cf(self):
        bool_filter = [col for col in self.Reads.columns if 'CF' in col or col == 'TLD Type']
        cf_df = self.Reads[bool_filter]
        styled_df = cf_df.style.apply(self.highlight_row, axis = 1)
        return styled_df, cf_df[cf_df['%SD CF'] > 3], cf_df
    
        
    def comp_stats(self):
        dtypes = ['nC', 'CF']
        for dtype in dtypes:  
            bool_filter = [col for col in self.Reads.columns if dtype in col]
            filtered_df = self.Reads[bool_filter]
            means = filtered_df.mean(axis=1)
            std_devs = filtered_df.std(axis=1)
            pct_SDs = (std_devs / means) * 100
            
            self.Reads[f'Mean {dtype}'] = means
            self.Reads[f'%SD {dtype}'] = pct_SDs
            
            for i, row in self.Reads.iterrows():
                for key in self.TLDs[i].info.keys():
                    if dtype in key:
                        if 'mean' in key:
                            self.TLDs[i].info[key] = means.iloc[i]
                        if 'SD' in key:
                            self.TLDs[i].info[key] = pct_SDs.iloc[i]
