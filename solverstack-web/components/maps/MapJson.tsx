import { useState, useEffect } from 'react';
import { json } from 'd3';


const jsonUrl: string = 'https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson';

const WorldAtlasJson = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    json(jsonUrl).then(function(data) { setData(data); });
  }, []);

  return data;
};

export default WorldAtlasJson;