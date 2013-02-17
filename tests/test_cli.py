import sys
from StringIO import StringIO
from tempfile import mkdtemp
import os
import shutil
import json

from unittest import TestCase
from nose.tools import eq_
from httpretty import httprettified
from mock import Mock

from triv.io import client as cli
from triv.io.client import api
import helper


class TestCli(object):
  """
  Test commands display the right output and obvious errors
  """
  
  def contains(self, msg):
    assert msg in self.output.getvalue(), 'stdout did not contain\n"{}"'.format(msg)
    
  def setUp(self):
    self.saved_cwd = os.getcwd()
    self.output = StringIO()
    self.saved_stdout = sys.stdout
    sys.stdout = self.output
    self.temp_dir = mkdtemp()
    self.cookie_dir = self.temp_dir#os.path.join(self.temp_dir, 'cookies')
    self.conn = helper.client(self.cookie_dir)
    os.chdir(self.temp_dir)

  def tearDown(self):
    self.output.close()
    sys.stdout = self.saved_stdout
    os.chdir(self.saved_cwd)
    shutil.rmtree(self.temp_dir)
  
  @httprettified  
  def test_login_exlpains_git_usage(self):
    helper.github_login_flow()
    cli.login_cmd(self.conn)
    self.contains("Triv.io uses github for authentication.")


  def test_create_new_project(self):
    session = Mock()
    session.create_project.return_value = api.Project(
      id="123",
      title="acceptance",
      repositories=[dict(
        git_url="https://github.com/trivio/acceptance.git",
        name="acceptance"
      )]
    )    
    

    cli.create_cmd(session, "acceptance")
    
    self.contains("Creating triv.io project")
    self.contains("Cloning repository")
    self.contains("Saving project settings to acceptance/.trivio.project")
    
    assert session.create_project.called
    assert os.path.isdir('acceptance') # command should create an directory
    assert os.path.isfile('acceptance/.trivio.project')
    assert os.path.isdir('acceptance/.git')

    
  def test_create_project_from_repo(self):
    session = Mock()

    session.create_project.return_value = api.Project(
      session=session,
      id="123",
      title="acceptance",
      repositories=[dict(
        git_url="https://github.com/trivio/acceptance.git",
        name="acceptance"
      )]
    )    
    
    cli.create_cmd(session, "https://github.com/trivio/acceptance.git")


    assert session.create_project.called
    assert os.path.isdir('acceptance') # command should create an directory
    assert os.path.isfile('acceptance/.trivio.project')
    assert os.path.isdir('acceptance/.git')
    assert os.path.isfile('acceptance/README')
    
    self.contains("Creating triv.io project")
    self.contains("Cloning repository")
    self.contains("Saving project settings to acceptance/.trivio.project")
    
  
    
    