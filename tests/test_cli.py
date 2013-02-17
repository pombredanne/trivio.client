import sys
from StringIO import StringIO

from unittest import TestCase
from nose.tools import eq_
from httpretty import httprettified

from triv.io import client as cli
import helper

from tempfile import mkdtemp
import os
import shutil

class TestCli(object):
  """
  Test commands display the right output and obvious errors
  """
  
  def contains(self, msg):
    assert msg in self.output.getvalue(), 'stdout did not contain\n"{}"'.format(msg)
    
  def setUp(self):
    self.output = StringIO()
    self.saved_stdout = sys.stdout
    sys.stdout = self.output
    self.cookie_dir = mkdtemp()
    self.conn = helper.client(self.cookie_dir)

  def tearDown(self):
    self.output.close()
    sys.stdout = self.saved_stdout
    shutil.rmtree(self.cookie_dir)
  
  @httprettified  
  def test_login_exlpains_git_usage(self):
    helper.github_login_flow()
    cli.login_cmd(self.conn)
    self.contains("Triv.io uses github for authentication.")
