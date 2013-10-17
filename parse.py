from xml.dom.minidom import parseString
import datetime

class TimexParse:
    xml_data = None

    def getData(self,indata):
        confin = open(indata,"rt")
        lines = confin.read()
        self.xml_data = parseString(lines)    
        confin.close() 

    def parseWoData(self):
        wo_data = {}
        list_of_data = self.xml_data.getElementsByTagName("workout")[0]
        athlete_data = list_of_data.getElementsByTagName("athlete")[0].childNodes
        for i in athlete_data:
            ret = i.childNodes[0]
            wo_data[i.nodeName] = ret.nodeValue
        return wo_data

    def parseSummaryData(self):
        summary_data = {}
        list_of_data = self.xml_data.getElementsByTagName("summarydata")[0]
        for i in list_of_data.childNodes:
            ret = i.childNodes
            if len(ret)>0:
                summary_data[i.nodeName] = ret[0].nodeValue
        return summary_data

    def parseSample(self):
        samples = []
        list_of_samples = self.xml_data.getElementsByTagName("sample")
        for i in list_of_samples:
            sample_data = {}
            for j in i.childNodes:
                ret = j.childNodes
                sample_data[j.nodeName] = ret[0].nodeValue
            samples.append(sample_data)
        return samples

    def parseExtensions(self):
        extensions=[]
        list_of_extensions = self.xml_data.getElementsByTagName("extension")
        for i in list_of_extensions:
            extenions_data = {}
            for j in i.childNodes:
                ret = j.childNodes
                extenions_data[j.nodeName] = ret[0].nodeValue
            extensions.append(extenions_data)
        return extensions


def parseSegment(a):
    cnt=1
    lngth = len(a.childNodes)
    data = []
    while cnt<lngth:
        data.append(showElements(a,"beginning"))
        data.append(showElements(a,"duration"))
        data.append(showElements(a,"durationstopped"))
        data.append(showElements(a,"work"))
        data.append(showElements(a,"hr"))
        data.append(showElements(a,"spd"))
        data.append(showElements(a,"dist"))
        data.append(showElements(a,"alt"))
        cnt+=1
    return data



def parseTimexData(lines):
    current_time = str(datetime.datetime.now()).replace(" ","T")+"Z"
    out_gpx = open("out.gpx","wt")
    out_gpx.write('<gpx version="1.1" creator="b0j3" ')
    out_gpx.write('xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/0" ')
    out_gpx.write('xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd">')
    out_gpx.write('<trk><name>ACTIVE LOG</name><trkseg>')

    ret = parseString(lines).childNodes
    for i in ret:
        #for j in i.childNodes:
            #for k in j.childNodes:
            #    for l in k.childNodes:
            #        text_data = l.nodeValue
            #        if text_data!=None:
            #            print text_data

        #print "Summary data:"
        #for a in i.getElementsByTagName("summarydata"):
        #    print parseSegment(a)
        #print "----"
        segment_data = {}        

        for a in i.getElementsByTagName("segment"):
            left = a.getElementsByTagName("name")[0].childNodes[0].nodeValue
            right = parseSegment(a)

            segment_data[left] = right

        hr_data = {}
        #duration_data = {}
        distance_data = {}

        for a in i.getElementsByTagName("sample"):
            cnt=0
            lngth = len(a.childNodes)
            while cnt<lngth:
                toff = showElements(a,"timeoffset")
                hr = showElements(a,"hr")
                distance = showElements(a,"dist")

                try:
                    hr_data[toff[1]]
                except:
                    hr_data[toff[1]]=int(float(hr[1]))

                try:
                    distance_data[toff[1]]
                except:
                    distance_data[toff[1]]=int(float(distance[1]))


                showElements(a,"spd")
                showElements(a,"dist")
                showElements(a,"lat")
                #write out gpx
                lat_data = a.getElementsByTagName("lat")[0].childNodes[0].nodeValue
                lon_data = a.getElementsByTagName("lon")[0].childNodes[0].nodeValue
                out_gpx.write("<trkpt lat='"+lat_data+"' lon='"+lon_data+"'>")
                out_gpx.write('  <ele>'+lat_data+'</ele><time>'+current_time+'</time></trkpt>')
                #end write
                showElements(a,"lon")
                showElements(a,"alt")            
                for b in a.getElementsByTagName("extension"):                        
                    showElements(b,"hrstatus")            
                    showElements(b,"compass")                            
                    showElements(b,"gpsspeed")                            
                    showElements(b,"gpsstatus")
                    showElements(b,"ftpodstatus")                            
                    showElements(b,"pmstatus")                            
                    showElements(b,"spdstatus")                            
                    showElements(b,"cadstatus")                            


                #print "hr "+str(a.getElementsByTagName("hr")[0].childNodes)
                #print a.childNodes
                cnt+=1
    out_gpx.write("</trkseg></trk></gpx>")
    out_gpx.close()
    return [segment_data,hr_data,distance_data]

if __name__ == "__main__":
    timex = TimexParse()

    timex.getData("test.pwx")
    print timex.parseWoData()
    print timex.parseSummaryData()
    print timex.parseSample()
    print timex.parseExtensions()
    
