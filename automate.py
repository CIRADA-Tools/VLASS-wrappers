def main():
    # Get user input for type and epochs
    image_type = input("Enter the image type (se or ql): ")
    epochs = input("Enter the epochs separated by commas (e.g., 1.1, 1.2, 2.1): ")

    # Create a list of epochs
    epoch_list = epochs.split(',')

    # Generate shell script content
    script_content = """#!/bin/bash

# Activate the appropriate environment
. /tmp/set_workdir.sh
echo "Activating environment..."
conda activate myenv

# Example: Navigate to the working directory
cd $PIPE1

# Get URLs and prepare manifest
echo "Fetching URLs from NRAO..."

"""

    # Handle the first epoch
    if epoch_list:
        first_epoch = epoch_list[0]
        if image_type == 'se':
            script_content += f'python get_urls_from_nrao.py "https://archive-new.nrao.edu/vlass/se_continuum_imaging/VLASS{first_epoch}/" w I\n'
        elif image_type == 'ql':
            script_content += f'python get_urls_from_nrao.py "https://archive-new.nrao.edu/vlass/quicklook/VLASS{first_epoch}/" w I\n'

    # Try to handle the rest of the epochs
    try:
        for epoch in epoch_list[1:]:
            if image_type == 'se':
                script_content += f'python get_urls_from_nrao.py "https://archive-new.nrao.edu/vlass/se_continuum_imaging/VLASS{epoch}/" a I\n'
            elif image_type == 'ql':
                script_content += f'python get_urls_from_nrao.py "https://archive-new.nrao.edu/vlass/quicklook/VLASS{epoch}/" a I\n'
    except IndexError:
        pass  # If there's only one epoch, just pass

    script_content += """
cp manifest.csv media/manifests/

# Execute Pipeline 1 steps
echo "Running Pipeline 1..."
rm -rf data
python3 catenator.py flush

# Run the Python script
python pipe1.py

# Change directory to the parent directory
cd ..


cp $PIPE1/data/products/CIRADA_VLASS*_table3_subtile_info*.csv $PIPE2/test_data/test_subtiles.csv
cp $PIPE1/data/products/VLASS*_UOFM_*_Catalogue_*.csv $PIPE2/test_data/test_pybdsf_catenator_out.csv
cd $PIPE2
nohup python3 component_table/vlass_compcat_vlad_stage2_yg.py test_data/test_pybdsf_catenator_out.csv  test_data/test_subtiles.csv  other_survey_data/CATALOG41.FIT other_survey_data/first_14dec17.fits > step1.out 
nohup python3 host_table/vlass_iso_and_cd_finding_v2.py VLASS_components.csv > step2.out 
cd host_table
mkdir LR_output
nohup python3 vlass_uw_lr_v2.py ../VLASS_source_candidates.csv ../other_survey_data/unWISE_coad_directory.csv > step3.out 
nohup python3 stack_matches_v1.py ../VLASS_source_candidates.csv ../VLASS_components.csv > step4.out 
cd ..
mv host_table/VLASS_table* .
nohup python3 finalise_cat/VLASSQL1CIR_catalogue_finalise.py VLASS_table1_components.csv VLASS_table2_hosts.csv test_data/test_subtiles.csv > step5.out 
python3 duplicate_ridder.py


echo "All epochs processed."

# Deactivate the environment
echo "Deactivating environment..."
conda deactivate


"""

    # Write to a shell script file
    with open('pipe1andpipe2.sh', 'w') as file:
        file.write(script_content)

    print("Shell script 'pipe1andpipe2.sh' has been generated.")

    script_content = """#!/bin/bash    
# Activate environment for Pipeline 3
echo "Activating cutoutenv for Pipeline 3..."
conda activate cutoutenv

# Prepare for cutout downloading
cd $PIPE3_1
cp $PIPE2/catalogue_output_files/*_duplicate_free.csv .

# Modify the vlass.py file
echo "Modifying vlass.py..."
"""

    # Comment out the existing line and insert the new condition for the first epoch

    # Add conditions for additional epochs
    try:
        for epoch in epoch_list[1:]:
            script_content += f"""
sed -i '1s/^/epoch2="{epoch}"\\n/' $PIPE3_1/core/vlass.py
"""
    except:
    	pass
    script_content += f"""
sed -i '1s/^/epoch2=epoch1\\n/' $PIPE3_1/core/vlass.py  

"""

# Modify the splitandcreate.sh file

    # Modify the line in splitandcreate.sh for each epoch
    # for epoch in epoch_list:
    script_content += f"""
sed -i 's/ORIGINAL_FILENAME="VLASS3QLCIR_components_duplicate_free.csv"/ORIGINAL_FILENAME="VLASS{epoch_list[0][0]}{image_type.upper()}CIR_components_duplicate_free.csv"/' $PIPE3_1/splitandcreate.sh
"""



    script_content += f"""
echo "Adding epoch1 and image_type to core/vlass.py..."
sed -i '1s/^/epoch1="{epoch_list[0]}"\\n/' $PIPE3_1/core/vlass.py
sed -i '1s/^/imagetype="{image_type}"\\n/' $PIPE3_1/core/vlass.py
. ./splitandcreate.sh  
python3 ../fix_headers.py 3
conda deactivate
conda activate sidelobe_pipe_env
cd $PIPE3_2
. ./pipe3_2.sh
conda deactivate
conda activate myenv
cd $PIPE4
python hunt_dragns_and_find_host.py $PIPE3_2/components_out_som.csv
"""
    if image_type == 'se':
        script_content += f"""
cd $PIPE1
mv media/manifests/manifest.csv media/manifests/manifest_I.csv

# Get URLs and prepare manifest
echo "Fetching alpha URLs from NRAO..."
"""

        # Handle the first epoch
        if epoch_list:
            first_epoch = epoch_list[0]
            script_content += f'python get_urls_from_nrao.py "https://archive-new.nrao.edu/vlass/se_continuum_imaging/VLASS{first_epoch}/" w alpha\n'
    
        # Try to handle the rest of the epochs
        try:
            for epoch in epoch_list[1:]:
                script_content += f'python get_urls_from_nrao.py "https://archive-new.nrao.edu/vlass/se_continuum_imaging/VLASS{epoch}/" a alpha\n'
        except IndexError:
            pass  # If there's only one epoch, just pass

    script_content += """
cp manifest.csv media/manifests/

# Execute Pipeline 1 steps
echo "Downloading alpha images"
python3 catenator.py flush
python3 catenator.py download
python3 ../fix_headers.py 1
mkdir $PIPE1/data/alpha/
mv $PIPE1/data/tiles/*/*alpha* $PIPE1/data/alpha/
python3 add_spix.py
"""

    # Comment out the existing line and insert the new condition for the first epoch

    # Add conditions for additional epochs


    script_content += f"""
echo "Adding epoch1 and image_type to finalize_catalogs.py..."
sed -i '1s/^/epoch="{epoch_list[0][0]}"\\n/' $PIPE1/finalize_catalogs.py
sed -i '1s/^/imagetype="{image_type}"\\n/' $PIPE1/finalize_catalogs.py

"""
    # Write to a shell script file
    with open('pipe3andpipe4.sh', 'w') as file:
        file.write(script_content)

    print("Shell script 'pipe3andpipe4.sh' has been generated.")

if __name__ == "__main__":
    main()