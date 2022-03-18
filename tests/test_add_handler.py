"""Unit tests for adding requirements."""
import shutil
import unittest
from pathlib import Path

from gamcore.gamconfig import GAMConfig
from gamcore.handlers.add import AddHandler
from gamcore.handlers.project import ProjectHandler
from gamcore.handlers.requirement import RequirementHandler


class AddHandlerTests(unittest.TestCase):
    def __init__(self, *args) -> None:
        gam_config = Path().cwd() / "gam_config/config.toml"
        self.config = GAMConfig.get_instance(gam_config)
        super(AddHandlerTests, self).__init__(*args)

    def test_gather_requirements(self) -> None:
        test_projects_dir = Path.cwd() / "test_projects"
        name = "test_gather_requirements"
        project_dir = test_projects_dir.joinpath(name)
        shutil.rmtree(project_dir, ignore_errors=True)
        project = ProjectHandler.new(test_projects_dir, name)
        # Add file dependency to requirement.
        file_dep_name = "test_gather_requirements_dep"
        file_dep_dir = test_projects_dir.joinpath(file_dep_name)
        shutil.rmtree(file_dep_dir, ignore_errors=True)
        file_dep_project = ProjectHandler.new(test_projects_dir, file_dep_name)
        file_dep_tarball = file_dep_project.build()
        project.details.dependencies[file_dep_name] = file_dep_tarball.as_posix()
        project.save()
        # TODO Add git dependency to requirement.
        # TODO Add repository dependency to requirement.
        # Test requirements.
        project_tarball = project.build()
        # Make the project itself the thing added since it had all the
        # dependencies.
        add_handler = AddHandler(
            project, RequirementHandler(project_tarball.resolve().as_posix())
        )
        add_handler._gather_requirements()
        self.assertEqual(
            [name, file_dep_name],
            [it.project_details.name for it in add_handler._unmet_requirements],
        )

    def test_execute_file_add(self) -> None:
        test_projects_dir = Path.cwd() / "test_projects"
        name = "test_file_add"
        project_dir = test_projects_dir.joinpath(name)
        shutil.rmtree(project_dir, ignore_errors=True)
        project = ProjectHandler.new(test_projects_dir, name)
        # Add file dependency to requirement.
        dep_name = "test_file_add_dep"
        dep_dir = test_projects_dir.joinpath(dep_name)
        shutil.rmtree(dep_dir, ignore_errors=True)
        dep_project = ProjectHandler.new(test_projects_dir, dep_name)
        # Create sample file with text.
        dep_file = dep_project.path.joinpath("src/some_file")
        dep_file.touch()
        dep_file.write_text("some text")
        dep_tarball = dep_project.build()
        project.details.dependencies[dep_name] = dep_tarball.as_posix()
        project.save()
        # Test add.
        add_handler = AddHandler(
            project, RequirementHandler(dep_tarball.resolve().as_posix())
        )
        add_handler.execute()
        self.assertEqual(
            "some text",
            project.path.joinpath("addons", dep_name, "some_file").read_text(),
        )
