from django.conf import settings
from django.db import models
from .validators import validate_file_extension

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    description = models.CharField(max_length=250, null=False, unique=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner_normalproject', on_delete=models.CASCADE)
    project_members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    public_status = models.BooleanField(default=0)
    collab_status = models.BooleanField(default=0)
    parallel_status = models.BooleanField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def is_public(self):
        return bool(self.public_status)

    def is_collab(self):
        return bool(self.collab_status)

    def get_project_members(self):
        return self.project_members

    def is_user_collaborator(self, user):
        list_col = self.get_project_members().all()
        if user in list_col:
            return True
        else:
            return False

    def get_owner(self):
        return self.owner

    def set_status_public(self, status):
        self.public_status=status

    def set_status_collab(self, status):
        self.collab_status=status

class Document(models.Model):
    project = models.ForeignKey(Project, related_name='project_document', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='owner_document', on_delete=models.CASCADE)

class File(models.Model):
    file = models.FileField(blank=False, null=False, upload_to='mediafiles/', validators=[validate_file_extension])
    name = models.CharField(max_length=100, null=False, unique=True)
    document = models.ForeignKey(Document, related_name='file_document', on_delete=models.CASCADE)
    tagged_doc = models.FileField(max_length=100, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def set_tagged_doc(self, file_url):
        self.tagged_doc = file_url

    def set_file(self, file_url):
        self.file = file_url

class Metadata(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    project = models.ManyToManyField(Project, blank=True)

class File_Metadata_Relation(models.Model):
    metadata = models.ForeignKey(Metadata, related_name='metadata', on_delete=models.CASCADE)
    file = models.ForeignKey(File, related_name='metadata_file', on_delete=models.CASCADE)
    data = models.CharField(max_length=250, blank=True, null=True)

