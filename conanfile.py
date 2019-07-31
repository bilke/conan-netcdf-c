from conans import ConanFile, CMake, tools


class NetcdfcConan(ConanFile):
    name = "netcdf-c"
    version = "4.6.2"
    license = "MIT"
    author = "Lars Bilke, lars.bilke@ufz.de"
    url = "https://github.com/bilke/conan-netcdf-c"
    description = "Unidata network Common Data Form"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    generators = "cmake"

    def source(self):
        self.run("git clone --depth=1 --branch v{0} https://github.com/Unidata/netcdf-c.git".format(self.version))
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("netcdf-c/CMakeLists.txt", "project(netCDF C)",
                              '''project(netCDF C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def requirements(self):
        self.requires("libcurl/7.61.1@bincrafters/stable")
        self.requires("hdf5/1.10.5-dm1@bilke/testing")
    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ENABLE_TESTS"] = False
        cmake.definitions["BUILD_UTILITIES"] = False
        cmake.configure(source_folder="netcdf-c")
        return cmake

    def configure(self):
        del self.settings.compiler.libcxx

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["netcdf"]

