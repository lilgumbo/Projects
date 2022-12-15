#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <algorithm>
#include <math.h>
#include "helperFunctions.cpp"
#define PI 3.14159265

//Create a raycast ppm from an input file describing the scene
int main(int argc, char** argv){    
    //Read file and map values to dictionary
    std::string input = "";
    input = readFile(argv[1]);
    std::map<std::string, std::vector<double>> map;
    std::vector<std::string> textures;
    std::string keywords[15] = {"eye", "viewdir", "updir", "vfov", "imsize", "bkgcolor", "mtlcolor", "sphere", "p", "light", "v", "vn", "vt", "f", "texture"};
    std::pair<std::map<std::string, std::vector<double>>, std::vector<std::string>> ret = extractValues(input, keywords);
    map = ret.first;
    textures = ret.second;
    std::cout << "----Map Created----" << std::endl;
    //print_map(map, keywords);

    //Store sphere objects into vector
    //STORE SPHERES
    std::vector<Shape> objs;
    std::vector<Texture> txtObjs;
    for(int i=0; i<map["sphere"].size(); i+=4){
        Sphere cur;
        objs.push_back(cur);
        objs[objs.size()-1].type = "sphere";
        objs[objs.size()-1].pos.push_back(map["sphere"][0+i]);
        objs[objs.size()-1].pos.push_back(map["sphere"][1+i]);
        objs[objs.size()-1].pos.push_back(map["sphere"][2+i]);
        objs[objs.size()-1].r = map["sphere"][3+i];
    }
    //STORE TRIANGLES
    for(int i=0; i<map["f"].size(); i+=9){
        Triangle cur;
        objs.push_back(cur);
        objs[objs.size()-1].type = "triangle";
        //assign vertex values
        double vertexIdx = map["f"][i];
        objs[objs.size()-1].v1.push_back(map["v"][(vertexIdx-1)*3]);
        objs[objs.size()-1].v1.push_back(map["v"][(vertexIdx-1)*3+1]);
        objs[objs.size()-1].v1.push_back(map["v"][(vertexIdx-1)*3+2]);
        vertexIdx = map["f"][i+3];
        objs[objs.size()-1].v2.push_back(map["v"][(vertexIdx-1)*3]);
        objs[objs.size()-1].v2.push_back(map["v"][(vertexIdx-1)*3+1]);
        objs[objs.size()-1].v2.push_back(map["v"][(vertexIdx-1)*3+2]);
        vertexIdx = map["f"][i+6];
        objs[objs.size()-1].v3.push_back(map["v"][(vertexIdx-1)*3]);
        objs[objs.size()-1].v3.push_back(map["v"][(vertexIdx-1)*3+1]);
        objs[objs.size()-1].v3.push_back(map["v"][(vertexIdx-1)*3+2]);
        //assign normal values
        double normalIdx = map["f"][i+2];
        if(normalIdx != 0){
            objs[objs.size()-1].vn1.push_back(map["vn"][(normalIdx-1)*3]);
            objs[objs.size()-1].vn1.push_back(map["vn"][(normalIdx-1)*3+1]);
            objs[objs.size()-1].vn1.push_back(map["vn"][(normalIdx-1)*3+2]);  
            normalIdx = map["f"][i+5];
            objs[objs.size()-1].vn2.push_back(map["vn"][(normalIdx-1)*3]);
            objs[objs.size()-1].vn2.push_back(map["vn"][(normalIdx-1)*3+1]);
            objs[objs.size()-1].vn2.push_back(map["vn"][(normalIdx-1)*3+2]);
            normalIdx = map["f"][i+8];
            objs[objs.size()-1].vn3.push_back(map["vn"][(normalIdx-1)*3]);
            objs[objs.size()-1].vn3.push_back(map["vn"][(normalIdx-1)*3+1]);
            objs[objs.size()-1].vn3.push_back(map["vn"][(normalIdx-1)*3+2]);
        }
        //assign texture values
        double textureIdx = map["f"][i+1];
        if(textureIdx != 0){
            objs[objs.size()-1].vt1.push_back(map["vt"][(textureIdx-1)*2]);
            objs[objs.size()-1].vt1.push_back(map["vt"][(textureIdx-1)*2+1]);
            textureIdx = map["f"][i+4];
            objs[objs.size()-1].vt2.push_back(map["vt"][(textureIdx-1)*2]);
            objs[objs.size()-1].vt2.push_back(map["vt"][(textureIdx-1)*2+1]);
            textureIdx = map["f"][i+7];
            objs[objs.size()-1].vt3.push_back(map["vt"][(textureIdx-1)*2]);
            objs[objs.size()-1].vt3.push_back(map["vt"][(textureIdx-1)*2+1]);
        }
    }
    //Store plane objects
    for(int i=0; i<map["p"].size(); i+=3){
        Plane cur;
        objs.push_back(cur);
        objs[objs.size()-1].type = "plane";
        double vertexIdx = map["p"][i];
        objs[objs.size()-1].v1.push_back(map["v"][(vertexIdx-1)*3]);
        objs[objs.size()-1].v1.push_back(map["v"][(vertexIdx-1)*3+1]);
        objs[objs.size()-1].v1.push_back(map["v"][(vertexIdx-1)*3+2]);
        vertexIdx = map["p"][i+1];
        objs[objs.size()-1].v2.push_back(map["v"][(vertexIdx-1)*3]);
        objs[objs.size()-1].v2.push_back(map["v"][(vertexIdx-1)*3+1]);
        objs[objs.size()-1].v2.push_back(map["v"][(vertexIdx-1)*3+2]);
        vertexIdx = map["p"][i+2];
        objs[objs.size()-1].v3.push_back(map["v"][(vertexIdx-1)*3]);
        objs[objs.size()-1].v3.push_back(map["v"][(vertexIdx-1)*3+1]);
        objs[objs.size()-1].v3.push_back(map["v"][(vertexIdx-1)*3+2]);
    }
    //Store material values
    for(int i=0; i<map["mtlcolor"].size(); i+=10){
        Pixel p1, p2;
        p1.red = map["mtlcolor"][0+i];
        p1.green = map["mtlcolor"][1+i];
        p1.blue = map["mtlcolor"][2+i];
        p2.red = map["mtlcolor"][3+i];
        p2.green = map["mtlcolor"][4+i];
        p2.blue = map["mtlcolor"][5+i];
        objs[(i/10)].mtl.orig = p1;
        objs[(i/10)].mtl.spec = p2;
        objs[(i/10)].mtl.ka = map["mtlcolor"][6+i];
        objs[(i/10)].mtl.kd = map["mtlcolor"][7+i];
        objs[(i/10)].mtl.ks = map["mtlcolor"][8+i];
        objs[(i/10)].mtl.n = map["mtlcolor"][9+i];
    }
    //Store texture values
    for(int i=0; i<textures.size(); i++){
        //Texture cur;
        //cur = readPpm(textures[i]);
        //txtObjs.push_back(cur);
    }
    //define viewing frame
    ViewingFrame viewingFrame;
    viewingFrame = initializeViewingFrame(map);

    //initialize array of pixels set to the background color
    std::cout << "----Creating Background----" << std::endl;
    Pixel bkg;
    bkg.red = map["bkgcolor"][0]*255;    
    bkg.green = map["bkgcolor"][1]*255;
    bkg.blue = map["bkgcolor"][2]*255;
    std::vector<std::vector<Pixel>> img;
    for(int y=0; y<map["imsize"][1]; y++){
        std::vector<Pixel> row;
        img.push_back(row);
        for(int x=0; x<map["imsize"][0]; x++){
            img[y].push_back(bkg);
        }
    }

    //begin at top left point and loop each pixel
    std::vector<double> curPoint = viewingFrame.ul;
    Ray ray;
    ray.dir = normalize(vectorAdd(curPoint, map["eye"], 0));
    ray.pos = map["eye"];
    
    std::cout << "----Generating Image----" << std::endl;
    for(int x=0; x<map["imsize"][0]; x++){
        for(int y=0; y<map["imsize"][1]; y++){
            //loop through every object and determine nearest intersection point
            double dist = -1; //distance to the nearest object
            int nearestIdx;
            for(int i=0; i<objs.size(); i++){
                //Find intersection and distance if shape is a sphere
                if(objs[i].type.compare("sphere") == 0){
                    double distanceToObj = rayToSphere(ray, objs[i]);
                    if(distanceToObj != -1 && (distanceToObj < dist || dist == -1)){
                        dist = distanceToObj;
                        nearestIdx = i;
                    }
                }   
                if((objs[i].type.compare("triangle") == 0) || 
                   (objs[i].type.compare("plane") == 0)){
                    double distanceToObj = rayToTriangle(ray, objs[i]);
                    if(distanceToObj != -1 && (distanceToObj < dist || dist == -1)){
                        dist = distanceToObj;
                        nearestIdx = i;
                    }
                }  
            }
            //if an intersection occurs, change the finals image's pixel color
            if(dist != -1){
                std::vector<int> S;
                std::vector<double> intersection;
                intersection.push_back(map["eye"][0] + dist*ray.dir[0]);
                intersection.push_back(map["eye"][1] + dist*ray.dir[1]);
                intersection.push_back(map["eye"][2] + dist*ray.dir[2]);
                //apply texture
                /*
                if(objs[nearestIdx].type.compare("triangle") == 0){
                    double u, v;
                    double imgI, imgJ;
                    u = objs[nearestIdx].vt1[0]*objs[nearestIdx].alpha +  
                        objs[nearestIdx].vt2[0]*objs[nearestIdx].beta +
                        objs[nearestIdx].vt3[0]*objs[nearestIdx].gamma;
                    v = objs[nearestIdx].vt1[1]*objs[nearestIdx].alpha + 
                        objs[nearestIdx].vt2[1]*objs[nearestIdx].beta +
                        objs[nearestIdx].vt3[1]*objs[nearestIdx].gamma;
                    //width and height of texture image
                    //imgI = round(u * (width - 1));
                    //imgJ = round(v * (height - 1)); 
                }*/
                //apply shadow and lighting
                S = shadowRay(intersection, map["light"], objs);
                Pixel adjusted = blinnPhong(objs[nearestIdx], map["light"], vectorScale(map["viewdir"], -1), intersection, S);
                img[y][x].red = adjusted.red*255;
                img[y][x].green = adjusted.green*255;
                img[y][x].blue = adjusted.blue*255;
            } 

            //update ray
            curPoint = vectorAdd(curPoint, viewingFrame.deltaV);
            ray.dir = normalize(vectorAdd(curPoint, map["eye"], 0));
        }
        //update ray
        curPoint[1] = viewingFrame.ul[1];
        curPoint = vectorAdd(curPoint, viewingFrame.deltaH);
        ray.dir = normalize(vectorAdd(curPoint, map["eye"], 0));
    }

    //Write image vector to output file "raycast.ppm"
    std::cout << "----Writing Image----" << std::endl;
    std::string outputfile = "raycast.ppm";
    std::ofstream output_stream(outputfile, std::ios::out | std::ios::binary);
    output_stream << "P3\n" << map["imsize"][0] << "\n" << map["imsize"][1] << "\n" << 255 << "\n";
    for(int y=0; y<map["imsize"][1]; y++){
        for(int x=0; x<map["imsize"][0]; x++){
            output_stream << img[y][x].red << " " << img[y][x].green << " " << img[y][x].blue << "\n";
        }
    }
    output_stream.close();
    return 0;
}
