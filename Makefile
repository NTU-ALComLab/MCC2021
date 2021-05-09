upload-folder = NTU-ALCom-SSAT

all:
	@zip -r $(upload-folder).zip bin/ starexec_description.txt
clean:
	@rm -rf $(upload-folder)/ $(upload-folder).zip
