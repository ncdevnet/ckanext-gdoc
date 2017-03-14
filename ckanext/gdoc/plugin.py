import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class GdocPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IResourceView)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'gdoc')

    def info(self):
        return {
            "name": "gdoc_view",
            "title": toolkit._('Google Doc Previewer'),
            "default_title": toolkit._('Preview'),
            "icon": "compass",
            "always_available": True,
            "iframed": False,
        }

    def setup_template_variables(self, context, data_dict):
        #print data_dict["resource"]['url']      
        from ckanext.cloudstorage.storage import ResourceCloudStorage
        rcs = ResourceCloudStorage(data_dict["resource"])
        import urllib
        import urlparse
        resource_url = rcs.get_url_from_filename(data_dict["resource"]["id"], urlparse.urlsplit(data_dict["resource"]["url"]).path.split('/')[-1])
        encoded_url = urllib.quote(resource_url)

        return {
            "resource_url": encoded_url
        }

    def can_view(self, data_dict):
        return data_dict['resource']['format'].lower() in ['doc', 'pdf', 'xls', 'xlsx']

    def view_template(self, context, data_dict):
        return "gdoc/preview.html"

    def form_template(self, context, data_dict):
        return "gdoc/form.html"