using System;
using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json.Linq;

namespace dofus_move_bot
{
    internal class DofusMap
    {
        public enum MapType
        {
            Incarnam,
            Enutrosor,
            Amakna,
            Xelorium,
            Srambad,
            Ecaflipus
        }

        private Dictionary<string, string> _map;

        public DofusMap()
            : this("Dofus.map")
        {
        }

        public DofusMap(string file)
        {
            _map = new Dictionary<string, string>();

            string json;
            using (var r = new StreamReader("Dofus.map"))
                json = r.ReadToEnd();

            var jObj = JObject.Parse(json);
            foreach (var (key, value) in jObj)
            {
                Console.WriteLine(key);

                if (value == null) continue;

                foreach (var content in value.Children<JObject>())
                    foreach (var prop in content.Properties())
                    {
                        Console.WriteLine(prop.Name);
                        Console.WriteLine(prop.Value);
                    }
            }
        }

        public bool GoTo(DofusPosition from, DofusPosition to)
        {
            throw new NotImplementedException();
        }

        public class DofusPosition
        {
            private const MapType DefaultMap = MapType.Incarnam;
            public readonly string repr;
            private MapType _mapType;

            private int _x;
            private int _y;

            public DofusPosition(MapType mapType, int x, int y)
            {
                _mapType = mapType;
                _x = x;
                _y = y;

                repr = x + "," + y;
            }

            public DofusPosition(int x, int y)
                : this(DefaultMap, x, y)
            {
            }

            public DofusPosition(MapType mapType, string repr)
            {
                _mapType = mapType;

                var coos = repr.Split(",");
                _x = int.Parse(coos[0]);
                _y = int.Parse(coos[1]);

                this.repr = repr;
            }

            public DofusPosition(string repr)
                : this(DefaultMap, repr)
            {
            }
        }
    }
}