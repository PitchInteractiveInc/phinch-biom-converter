import  webapp2, os, mimetypes, h5py, tempfile, contextlib, convert

htmlstart = """
	<!DOCTYPE html>
	<html lang="en">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width">
		<title>PHINCH - MDF5 to JSON biom converter</title>
		<link rel="stylesheet" href="static/utility.css">
		<link rel="stylesheet" href="static/style.css">
	</head>
	<div class="header">
		<a href="http://phinch.org/" target="_blank">
			<p class="logo">
				<img src="/static/phinch.png" height="50px">
			</p>
		</a>
	</div>
	"""
initmessage = '<div id="message"><a href="/clear"><div class="message" class="transition-background" style="display:none"></div></a></div>'
message = initmessage
htmlend = """
	<div class="top_sec">
		<div class="fileContainer">
			<form class="frmUpload form-horizontal" enctype="multipart/form-data" action="/upload" method="POST" onsubmit="return showMessage()">
				<input class="inputfile" id="file" name="files" type="file" />
				<label for="file"><div id="field" class="field">Drop File Here or Browse</div><div class="browse transition-background">BROWSE</div></label>
				<button class="parse transition-background file_btn" type="submit">CONVERT FILE</button>
			</form>
		</div>
	</div>
	<div class="about">
		<h1>
			Convert a HDF5 BIOM file to a JSON BIOM file for use with Phinch
		</h1>
		<p class="description"><a href="http://phinch.org/">Phinch</a> works with <a href="http://biom-format.org/">BIOM</a> file type 1.0, which is formatted as JSON. This is the file format produced by <a href="http://qiime.org/">QIIME</a> version 1.8 and earlier. If you're using a newer version of <a href="https://qiime2.org/">QIIME</a>, it will produce <a href="http://biom-format.org/">BIOM</a> file type 2.1, which is formatted as HDF5.</p>
		<p class="description">It's possible to convert the HDF5 tables into JSON tables using recent versions of <a href="https://qiime2.org/">QIIME</a> or the <a href="http://biom-format.org/documentation/biom_format.html">biom-format</a> package. The following command will create a new JSON-formatted <a href="http://biom-format.org/">BIOM</a> file: </p>
		<p class="description" style="background:#E5E6E8; text-align:center;"><code>biom convert -i otu_table.biom -o otu_table_json.biom --table-type="OTU table" --to-json</code></p>
		<p class="description">Alternatively, you can use <a href="http://link-to-the-tool-tk.com">this web-based tool</a> to convert an HDF5-formatted <a href="http://biom-format.org/">BIOM</a> file to a JSON-formatted <a href="http://biom-format.org/">BIOM</a> file that will work with <a href="http://phinch.org/">Phinch</a>.</p>
		<a href="http://phinch.org/" target="_blank">
			<button class="parse transition-background file_btn">RETURN TO PHINCH</button>
		</a>
	</div>
	<script type="text/javascript">
		var inputs = document.querySelectorAll( '.inputfile' );
		Array.prototype.forEach.call( inputs, function( input ) {
			var label = input.nextElementSibling,
				labelVal = label.innerHTML;
			input.addEventListener( 'change', function( e ) {
				var fileName = e.target.value.split('\\\\').pop();
				if( fileName )
					label.querySelector( '#field' ).innerHTML = fileName;
				else
					label.innerHTML = labelVal;
			});
		});
		function showMessage() {
			var message = document.querySelector ( '#message' );
			message.outerHTML = '<div id="message" class="message transition-background">Converting...</div>'
			//<a href="/clear"></a>
			return true;
		}
	</script>
	</body>
	</html>
	"""

class HomeHandler(webapp2.RequestHandler):
	def get(self):
		global message
		html = htmlstart + message + htmlend;
		self.response.write(html)

class ClearHandler(webapp2.RequestHandler):
	def get(self):
		global message
		message = initmessage
		self.redirect('/')
		
class StaticFileHandler(webapp2.RequestHandler):
    def get(self, path):
        abs_path = os.path.abspath(os.path.join(self.app.config.get('webapp2_static.static_file_path', 'static'), path))
        if os.path.isdir(abs_path) or abs_path.find(os.getcwd()) != 0:
            self.response.set_status(403)
            return
        try:
            f = open(abs_path, 'r')
            self.response.headers.add_header('Content-Type', mimetypes.guess_type(abs_path)[0])
            self.response.out.write(f.read())
            f.close()
        except:
            self.response.set_status(404)

class UploadHandler(webapp2.RequestHandler):
	def post(self):
		global message
		files = self.request.POST.getall('files')
		_files = [{'content': f.file.read(), 'filename': f.filename} for f in files if f is not u'']
		if len(_files) < 1:
			message = initmessage
			self.redirect('/')
		for f in _files:
			if f['content'][0:8] == b'\x89HDF\r\n\x1a\n':
				file_access_property_list = h5py.h5p.create(h5py.h5p.FILE_ACCESS)
				file_access_property_list.set_fapl_core(backing_store=False)
				file_access_property_list.set_file_image(f['content'])
				file_id_args = {
					'fapl': file_access_property_list,
					'flags': h5py.h5f.ACC_RDONLY,
					'name': next(tempfile._get_candidate_names()).encode(),
				}
				h5_file_args = {'backing_store': False, 'driver': 'core', 'mode': 'r'}
				with contextlib.closing(h5py.h5f.open(**file_id_args)) as file_id:
					with h5py.File(file_id, **h5_file_args) as h5_file:
						json = convert.tojson(h5_file)
						self.response.headers['Content-Type'] = 'application/json';
						self.response.headers['Content-Disposition'] = 'attachment; filename=%s' % f['filename']
						self.response.write(json)
						message = initmessage
						# self.redirect('/')
			else: 
				message = '<div id="message"><a href="/clear"><div class="message" class="transition-background">That file doesn\'t use the HDF5 format</div></a></div>'
				self.redirect('/')

app = webapp2.WSGIApplication([
	('/', HomeHandler),
	('/clear', ClearHandler),
	('/upload', UploadHandler),
	('/static/(.+)', StaticFileHandler)
], debug=True)

def main():
	from paste import httpserver
	httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
	main()
