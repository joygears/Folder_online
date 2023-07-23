const injection = () => {
  const WEBVTT = 'webvtt-lssdh-ios8';
  const MANIFEST_URL = "manifest";
  const forceSubs = localStorage.getItem('NSD_force-all-lang') !== 'false';

  // hijack JSON.parse and JSON.stringify functions
  ((parse, stringify) => {
    JSON.parse = function (text) {
      const data = parse(text);
      if (data && data.result && data.result.timedtexttracks && data.result.movieId) {
        window.dispatchEvent(new CustomEvent('netflix_sub_downloader_data', {detail: data.result}));
        console.log('manifest:')
        console.log(data)
        console.log(stringify(data))
      }
      return data;
    };
    JSON.stringify = function (data) {
      if (data && typeof data.url === 'string' && data.url.indexOf(MANIFEST_URL) > -1) {
        for (let v of Object.values(data)) {
          try {
            if (v.profiles)
              v.profiles.unshift(WEBVTT);
            if (v.showAllSubDubTracks != null && forceSubs)
              v.showAllSubDubTracks = true;
          }
          catch (e) {
            if (e instanceof TypeError)
              continue;
            else
              throw e;
          }
        }
        console.log('manifest_req:')
        console.log(data)
      }
      if(data && typeof data.movieId === 'number') {
        try {
          let videoId = data.params.sessionParams.uiplaycontext.video_id;
          if(typeof videoId === 'number' && videoId !== data.movieId)
            window.dispatchEvent(new CustomEvent('netflix_sub_downloader_data', {detail: {id_override: [videoId, data.movieId]}}));
        }
        catch(ignore) {}
      }
      return stringify(data);
    };
  })(JSON.parse, JSON.stringify);
}

injection();