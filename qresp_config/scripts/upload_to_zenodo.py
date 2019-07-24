import shutil
import requests
import os
import json
import sys

class UploadToZenodo:
    """ Upload Files to Zenodo
    """
    def __init__(self, ACCESS_TOKEN, path, metadata):
        self.headers = {"Content-Type": "application/json"}
        self.params = {'access_token': ACCESS_TOKEN}
        self.base_url = "https://sandbox.zenodo.org"
        self.deposition_id = self.generateDepositionId()
        self.acceptedExtentions = (".jpg", ".jpeg", ".png", ".gif", ".tiff", ".pdf", ".bmp", ".ico", ".svg")
        self.metadata = metadata
        self.path = path

    def generateDepositionId(self):
        """ Generates Deposition Id needed for identifying paper
        """
        response = requests.post('{base_url}/api/deposit/depositions'.format(base_url=self.base_url),
                                 params=self.params,
                                 json={}, headers=self.headers)
        if response.status_code >= 400:
            sys.exit(response.json())
        return response.json()['id']

    def uploadImagesToZenodo(self):
        """ Extracts Images from path and uploads to zenodo
            :param: path Directory or path to directory to upload data from
        """
        for r, d, f in os.walk(self.path):
            for file in f:
                if file.lower().endswith(self.acceptedExtentions):
                    data = {'filename': str(file)}
                    filepath = os.path.join(r, file)
                    files = {'file': open(str(filepath), 'rb')}
                    resp = requests.post(
                        '{base_url}/api/deposit/depositions/{deposition_id}/files'.format(base_url=self.base_url,
                                                                                          deposition_id=self.deposition_id),
                        params=self.params,
                        data=data, files=files)
                    if resp.status_code >= 400:
                        sys.exit(resp.json())
        print("Uploaded images to deposition id ", self.deposition_id)

    def uploadZipFileToZenodo(self):
        """ Converts folder to a zip file and uploads to zenodo
            :param: path Directory or path to directory to upload data from
        """
        filename = os.path.basename(self.path)
        archive_from = os.path.dirname(self.path)
        archive_to = os.path.basename(self.path.strip(os.sep))
        shutil.make_archive(filename, "zip", archive_from, archive_to)
        data = {'filename': str(filename) + ".zip"}
        files = {'file': open(str(filename) + ".zip", 'rb')}
        resp = requests.post('{base_url}/api/deposit/depositions/{deposition_id}/files'.format(base_url=self.base_url,
                                                                                               deposition_id=self.deposition_id),
                             params=self.params,
                             data=data, files=files)
        if resp.status_code >= 400:
            sys.exit(resp.json())
        print("Uploaded directory as a zip file ", self.deposition_id)

    def uploadMetadaFileToZenodo(self):
        """ Adds metadata to the deposition
        """
        resp = requests.put('{base_url}/api/deposit/depositions/{deposition_id}'.format(base_url=self.base_url,
                                                                                        deposition_id=self.deposition_id),
                            params=self.params,
                            data=json.dumps(self.metadata),
                            headers=self.headers)
        if resp.status_code >= 400:
            sys.exit(resp.json())
        print("Uploaded metadata file")

    def publishProjectToZenodo(self):
        """ Publishes metadata to zenodo
        """
        resp = requests.post(
            '{base_url}/api/deposit/depositions/{deposition_id}/actions/publish'.format(base_url=self.base_url,
                                                                                        deposition_id=self.deposition_id),
            params=self.params,
            headers=self.headers)
        if resp.status_code >= 400:
            sys.exit(resp.json())
        print("Published to zenodo")
        return resp.json()