#include <vector>
#include <math.h>
#include <iostream>
#include <fstream>
#include <map>
#include <algorithm>
#define PI 3.14159265

typedef struct{
    std::vector<double> ul, ur, br, bl, deltaH, deltaV;
} ViewingFrame;
typedef struct{
    std::vector<double> pos;
    std::vector<double> dir;
} Ray;
typedef struct{
    double red;
    double green;
    double blue;
} Pixel;
typedef struct{
    Pixel orig;
    Pixel spec;
    double ka, kd, ks, n;
} Material;
typedef struct{
    double r;
    std::vector<double> pos, v1, v2, v3, vn1, vn2, vn3, vt1, vt2, vt3;;
    std::string type;
    Material mtl;
    double alpha, beta, gamma;
} Shape;
struct Plane : Shape{
    std::string type;
    std::vector<double> v1, v2, v3;
    Material mtl;
};
struct Triangle : Shape{
    std::string type;
    std::vector<double> v1, v2, v3;
    std::vector<double> vn1, vn2, vn3;
    std::vector<double> vt1, vt2, vt3;
    Material mtl;
    double alpha, beta, gamma;
};
struct Sphere : Shape{
    std::string type;
    double r;
    std::vector<double> pos;
    Material mtl;
};
typedef struct{
    int width, height;
    std::vector<std::vector<Pixel>> image;
} Texture;

//Vector addition, addition=0 would result in subtraction
std::vector<double> vectorAdd(std::vector<double> v1, std::vector<double> v2, int addition=1){
    std::vector<double> v3;
    double sum;
    if(addition){
        for(int i=0; i<v1.size(); i++){
            sum = v1[i] + v2[i];
            v3.push_back(sum);
        }
    }else{
        for(int i=0; i<v1.size(); i++){
            sum = v1[i] - v2[i];
            v3.push_back(sum);
        }
    }
    return v3;
}

//Multiply vector by a scalar
std::vector<double> vectorScale(std::vector<double> v, double s){
    for(int i=0; i<v.size(); i++){
        v[i] = v[i] * s;
    }
    return v;
}

//Normalize a vector
std::vector<double> normalize(std::vector<double> v){
    std::vector<double> norm;
    //Find euclidean distance
    double total = 0;
    for(int i=0; i < v.size(); i++){
        total += v[i] * v[i];
    }
    double dist = sqrt(total);
    //Divide each array element by distance
    for(int i=0; i < v.size(); i++){
        norm.push_back(v[i] / dist);
    }
    return norm;
}

//Print a vector
void printVector(std::vector<double> v){
    for(int i=0; i<v.size(); i++){
        std::cout << v[i] << " ";
    }
    std::cout << "\n";
}

//Find cross product of a vector
std::vector<double> crossProduct(std::vector<double> vect_A, std::vector<double> vect_B){
    std::vector<double> cross_P(3);
    cross_P[0] = vect_A[1] * vect_B[2] - vect_A[2] * vect_B[1];
    cross_P[1] = vect_A[2] * vect_B[0] - vect_A[0] * vect_B[2];
    cross_P[2] = vect_A[0] * vect_B[1] - vect_A[1] * vect_B[0];
    return cross_P;
}

//Find dot product of a vector
double dotProduct(std::vector<double> vect_A, std::vector<double> vect_B){
    double product = 0;
    for(int i=0; i<vect_A.size(); i++){
        product += vect_A[i] * vect_B[i];
    }
    return product;
}

//Determine if a string is a number
bool isNumber(std::string number){
    if(number == " "){
        return false;
    }
    for (int i=0; i < number.length(); i++){
        if(number[0] == '-' || number[i] == '.'){
            continue;
        }
        if(!isdigit(number[i])){
            return false;
        }
    }
    return true;
}

//Convert string to vector by every " "
std::vector<double> stringToVector(std::string str){
    //remove double spaces
    for(int i=0; i<str.length(); i++){
        if(str[i] == ' ' && (str[i+1] == ' ' || i == 0)){
            str.erase(i, 1);
        }
    }    
    std::vector<double> v;
    int idx = str.find_first_of(" ");
    int len = str.length();
    std::string next = str;
    std::string val;
    while(idx != std::string::npos){
        val = next.substr(0, idx);
        if(isNumber(val)){
            v.push_back(stod(val));
        }else{
            std::cout << "invalid string: " << val << "\n";
            return {-1};
        }
        next = next.substr(idx+1, len-idx);
        idx = next.find_first_of(" ");
    }
    val = next;
    if(isNumber(val)){
        v.push_back(stod(val));
    }else{
        std::cout << "invalid string" << val << "\n";
        return {-1};
    }
    return v;
}

//Convert string to 2d array for triangles
std::vector<std::vector<double>> triangleStrToVector(std::string str){
    //remove double spaces
    for(int i=0; i<str.length(); i++){
        if(str[i] == ' ' && (str[i+1] == ' ' || i == 0)){
            str.erase(i, 1);
        }
    }    
    std::vector<std::vector<double>> v;
    int idx = str.find_first_of(" ");
    int len = str.length();
    std::string next = str;
    std::string val;
    std::vector<double> newVec;
    std::string checker;
    std::string v1, v2, v3;
    while(idx != std::string::npos){
        val = next.substr(0, idx);
        //if no texture or normal values are present
        if(val.find_first_of('/') == std::string::npos){
            if(isNumber(val)){
                newVec.push_back(stod(val));
                newVec.push_back(0);
                newVec.push_back(0);
                v.push_back(newVec);
            }else{
                std::cout << "invalid string: " << val << "\n";
                return {{-1}};
            }
        }
        //if value contains a slash
        else{
            int slash = val.find_first_of('/');
            checker = val.substr(slash+1, val.size());
            //in form v/vt
            if(checker.find_first_of('/') == std::string::npos){
                v1 = val.substr(0, slash);
                v2 = val.substr(slash+1, val.size());
                if(isNumber(v1) && isNumber(v2)){
                    newVec.push_back(stod(v1));
                    newVec.push_back(stod(v2));
                    newVec.push_back(0);
                }
            }
            //in form v/vt/vn or v//vn
            else{
                int slash2 = checker.find_first_of('/');
                v1 = val.substr(0, slash);
                v2 = val.substr(slash+1, slash2);
                v3 = checker.substr(slash2+1, checker.size());
                if(v2.compare("") == 0){
                    v2 = '0';
                }
                if(isNumber(v1) && isNumber(v2) && isNumber(v3)){
                    newVec.push_back(stod(v1));
                    newVec.push_back(stod(v2));
                    newVec.push_back(stod(v3));
                }
            }
            v.push_back(newVec);
        }
        next = next.substr(idx+1, len-idx);
        idx = next.find_first_of(" ");
        newVec.clear();
    }
    val = next;
    if(val.find_first_of('/') == std::string::npos){
        if(isNumber(val)){
            newVec.push_back(stod(val));
            newVec.push_back(0);
            newVec.push_back(0);
            v.push_back(newVec);
        }else{
            std::cout << "invalid string: " << val << "\n";
            return {{-1}};
        }
    }else{
        int slash = val.find_first_of('/');
        checker = val.substr(slash+1, val.size());
        //in form v/vn
        if(checker.find_first_of('/') == std::string::npos){
            v1 = val.substr(0, slash);
            v2 = val.substr(slash+1, val.size());
            if(isNumber(v1) && isNumber(v2)){
                newVec.push_back(stod(v1));
                newVec.push_back(stod(v2));
                newVec.push_back(0);
            }
        }
        //in form v/vt/vn or v//vn
        else{
            int slash2 = checker.find_first_of('/');
            v1 = val.substr(0, slash);
            v2 = val.substr(slash+1, slash2);
            v3 = checker.substr(slash2+1, checker.size());
            if(v2.compare("") == 0){
                v2 = '0';
            }
            if(isNumber(v1) && isNumber(v2) && isNumber(v3)){
                newVec.push_back(stod(v1));
                newVec.push_back(stod(v2));
                newVec.push_back(stod(v3));
            }
        }
        v.push_back(newVec);
    }
    return v;
}

//Read values from an input string and map keywords to a vector
std::pair<std::map<std::string, std::vector<double>>, std::vector<std::string>> extractValues(std::string input, std::string keywords[15]){
    std::map<std::string, std::vector<double>> map;
    std::vector<std::string> textures;
    std::pair<std::map<std::string, std::vector<double>>, std::vector<std::string>> pair;
    int next;
    while(input != ""){
        next = input.find_first_of("\n");
        std::string line = input.substr(0, next);
        std::string key = line.substr(0, line.find_first_of(' '));
        for(int i=0; i<15; i++){
            if(keywords[i] == key){
                //special case for texture
                if(key == "texture"){
                    textures.push_back(line.substr(line.find_first_of(' ')+1, line.length()));
                    continue;
                }
                //special case for triangle
                if(key == "f"){
                    std::vector<std::vector<double>> vec = triangleStrToVector(line.substr(line.find_first_of(' ')+1, line.length()));                    
                    for(int j=0; j<vec.size(); j++){                        
                        map[keywords[i]].push_back(vec[j][0]);
                        map[keywords[i]].push_back(vec[j][1]);
                        map[keywords[i]].push_back(vec[j][2]);
                    }
                    continue;
                }
                //convert string into vector
                std::vector<double> vec = stringToVector(line.substr(line.find_first_of(' ')+1, line.length()));
                //write vector to map
                for(int j=0; j<vec.size(); j++){
                    map[keywords[i]].push_back(vec[j]);
                }
            }
        }
        input = input.substr(next+1, input.length());
    }
    pair.first = map;
    pair.second = textures;
    return pair;
}

//Apply gradient according to the Blinn-Phong model
Pixel blinnPhong(Shape sphere, std::vector<double> light, std::vector<double> V, std::vector<double> intersection, std::vector<int> S){
    Pixel adjusted;
    std::vector<double> N, L, H, center, e1, e2;
    if(sphere.type.compare("sphere") == 0){
        center.push_back(sphere.pos[0]);
        center.push_back(sphere.pos[1]);
        center.push_back(sphere.pos[2]);
        double rInverse = (double)1/sphere.r;
        N = normalize(vectorScale(vectorAdd(intersection, center, 0), rInverse));
    }
    if(sphere.type.compare("triangle") == 0){
        e1 = vectorAdd(sphere.v2, sphere.v1, 0);
        e2 = vectorAdd(sphere.v3, sphere.v1, 0);
        N = crossProduct(e1, e2);
    }
    L.push_back(0);
    L.push_back(0);
    L.push_back(0);
    adjusted.red = (sphere.mtl.ka * sphere.mtl.orig.red);
    adjusted.green = (sphere.mtl.ka * sphere.mtl.orig.green);
    adjusted.blue = (sphere.mtl.ka * sphere.mtl.orig.blue);
    for(int i=0; i<light.size(); i+=7){
        L[0] = light[0+i];
        L[1] = light[1+i];
        L[2] = light[2+i];
        if(light[3+i] == 0){     //directional light
            L = normalize(vectorScale(L, -1));
        }else{      //point light
            L = normalize(vectorAdd(L, intersection, 0));
        }
        H = normalize(vectorAdd(L, V));
        adjusted.red += S[(i/7)] * light[4+i] * ((sphere.mtl.kd * sphere.mtl.orig.red * std::max((double)0, dotProduct(N, L))) + 
                        (sphere.mtl.ks * sphere.mtl.spec.red * std::pow(std::max((double)0, dotProduct(N, H)), sphere.mtl.n)));
        adjusted.green += S[(i/7)] * light[5+i] * ((sphere.mtl.kd * sphere.mtl.orig.green * std::max((double)0, dotProduct(N, L))) + 
                          (sphere.mtl.ks * sphere.mtl.spec.green * std::pow(std::max((double)0, dotProduct(N, H)), sphere.mtl.n)));    
        adjusted.blue += S[(i/7)] * light[6+i] * ((sphere.mtl.kd * sphere.mtl.orig.blue * std::max((double)0, dotProduct(N, L))) + 
                         (sphere.mtl.ks * sphere.mtl.spec.blue * std::pow(std::max((double)0, dotProduct(N, H)), sphere.mtl.n)));
    }
    return adjusted;
}

//Determine if a ray intersects a sphere (return -1 if no intersection)
double rayToSphere(Ray ray, Shape sphere){
    double t1, t2, B, C;
    double t3 = -1;

    B = 2*(ray.dir[0]*(ray.pos[0] - sphere.pos[0]) +
           ray.dir[1]*(ray.pos[1] - sphere.pos[1]) + 
           ray.dir[2]*(ray.pos[2] - sphere.pos[2]));

    C = pow((ray.pos[0] - sphere.pos[0]), 2) + 
        pow((ray.pos[1] - sphere.pos[1]), 2) + 
        pow((ray.pos[2] - sphere.pos[2]), 2) - 
        pow(sphere.r, 2);

    double discriminant = pow(B, 2) - (4*C);

    if(discriminant >= 0){
        t1 = std::max((double)0, (-B + sqrt(discriminant)) / 2);
        t2 = std::max((double)0, (-B - sqrt(discriminant)) / 2);
        t3 = std::min(t1, t2);
    }
    return t3;
}

//Determine if a ray intersects a triangle (return -1 if no intersection)
double rayToTriangle(Ray ray, Shape triangle){
    double t, D, denominator, numerator, beta, gamma, alpha, x, xb, xy;
    std::vector<double> e1, e2, n, intersection;
    t = -1;
    e1 = vectorAdd(triangle.v2, triangle.v1, 0);
    e2 = vectorAdd(triangle.v3, triangle.v1, 0);
    n = crossProduct(e2, e1);
    denominator = (n[0]*ray.dir[0] + n[1]*ray.dir[1] + n[2]*ray.dir[2]);
    //determine if ray intersects plane
    if(denominator != 0){
        D = -1*(n[0]*triangle.v1[0] + n[1]*triangle.v1[1] + n[2]*triangle.v1[2]);
        numerator = -1*(n[0]*ray.pos[0] + n[1]*ray.pos[1] + n[2]*ray.pos[2] + D);
        t = numerator/denominator;
        //ignore further restictions if the object is a plane
        if(triangle.type.compare("plane") == 0){
            return t;
        }
        intersection.push_back(ray.pos[0] + t*ray.dir[0]);
        intersection.push_back(ray.pos[1] + t*ray.dir[1]);
        intersection.push_back(ray.pos[2] + t*ray.dir[2]);
        std::vector<double> ep = vectorAdd(intersection, triangle.v1, 0);
        double d11, d12, d22, dp1, dp2;
        d11 = dotProduct(e1, e1);
        d12 = dotProduct(e1, e2);
        d22 = dotProduct(e2, e2);
        dp1 = dotProduct(ep, e1);
        dp2 = dotProduct(ep, e2);
        x = d11*d22 - d12*d12;
        xb = d22*dp1 - d12*dp2;
        xy = d11*dp2 - d12*dp1;
        triangle.beta = xb/x;
        triangle.gamma = xy/x;
        triangle.alpha = 1-(triangle.beta+triangle.gamma);
        //If outside of triangle, return -1
        if((triangle.beta+triangle.gamma) < 0 || (triangle.beta+triangle.gamma) > 1){
            return -1;
        }
        if(triangle.beta < 0 || triangle.gamma < 0 || triangle.beta > 1 || triangle.gamma > 1){
            return -1;
        }
    }
    return t;
}

std::vector<int> shadowRay(std::vector<double> intersection, std::vector<double> light, std::vector<Shape> objs){
    std::vector<int> S;
    double dist, lightDist;
    std::vector<double> cur;
    cur.push_back(0);
    cur.push_back(0);
    cur.push_back(0);
    Ray ray;
    ray.pos = intersection;
    for(int i=0; i<light.size(); i+=7){
        S.push_back(1);
        cur[0] = light[0+i];
        cur[1] = light[1+i];
        cur[2] = light[2+i];
        if(light[3+i] == 1){
            ray.dir = normalize(vectorAdd(ray.pos, cur, 0));
        }else{
            ray.dir = vectorScale(cur, -1);
        }
        lightDist = sqrt(pow((cur[0]-intersection[0]), 2) + pow((cur[1]-intersection[1]), 2) + pow((cur[2]-intersection[2]), 2));
        for(int j=0; j<objs.size(); j++){
            //Shadow ray for sphere collisions
            if(objs[j].type.compare("sphere") == 0){
                dist = rayToSphere(ray, objs[j]); 
            }
            if(objs[j].type.compare("triangle") == 0){
                dist = rayToTriangle(ray, objs[j]);
            }
            if((dist > 0.01) && (dist < lightDist || light[3+i] == 0)){
                S[(i/7)] = 0;
                break;
            }
        }
    }
    return S;
}

std::string readFile(std::string arg){
    std::cout << "----Reading Input File----" << std::endl;
    std::fstream fp;
    std::string input = "";
    fp.open(arg, std::ios::in);
    if(!fp){
        std::cout << "file not found";
        return 0;
    }else{
        std::string str;
        while(std::getline(fp, str)){
            input += str;
            input.push_back('\n');
        }
    }
    fp.close();
    return input;
}

Texture readPpm(std::string arg){
    std::fstream fp;
    std::string input = "";
    Texture cur;
    int iteration = 0;
    fp.open(arg, std::ios::in);
    if(!fp){
        std::cout << "!! Texture file not found !!" << std::endl;
        return cur;
    }else{
        std::string str;
        while(std::getline(fp, str)){
            if(iteration == 1){
                if(isNumber(str)){
                    cur.width = stoi(str);
                }
            }
            if(iteration == 2){
                if(isNumber(str)){
                    cur.height = stoi(str);
                }
            }
            input += str;
            input.push_back('\n');
            iteration++;
        }
    }
    /*
    Pixel px;
    //create 2d array of pixels for the texture
    for(int x=0; x<cur.width; x++){
        std::vector<Pixel> row;
        cur.image.push_back(row);
        for(int y; y<cur.height; y++){
            cur.image[y].push_back(px);
        }
    }
    */
    fp.close();
    return cur;
}

ViewingFrame initializeViewingFrame(std::map<std::string, std::vector<double>> map){
    ViewingFrame VF;
    std::vector<double> u = crossProduct(map["viewdir"], map["updir"]); //unit vector of viewing coordinate system
    std::vector<double> v = crossProduct(u, map["viewdir"]); //orthogonal to u
    u = normalize(u);
    v = normalize(v);
    double d = 25; //arbitrary distance
    double viewHeight = 2 * d * tan(map["vfov"][0]/2 * PI / 180.0);
    double aspectRatio = map["imsize"][0] / map["imsize"][1];
    double viewWidth = viewHeight * aspectRatio;
    std::vector<double> n = normalize(map["viewdir"]);
    std::vector<double> new1 = vectorScale(n, d);
    std::vector<double> new2 = vectorScale(u, viewWidth/2);
    std::vector<double> new3 = vectorScale(v, viewHeight/2);
    VF.ul = vectorAdd(vectorAdd(vectorAdd(map["eye"], new1), new2, 0), new3);
    VF.ur = vectorAdd(vectorAdd(vectorAdd(map["eye"], new1), new2), new3);
    VF.br = vectorAdd(vectorAdd(vectorAdd(map["eye"], new1), new2), new3, 0);
    VF.bl = vectorAdd(vectorAdd(vectorAdd(map["eye"], new1), new2, 0), new3, 0);
    VF.deltaH = vectorScale(vectorAdd(VF.ur, VF.ul, 0), 1/(map["imsize"][0]-1));
    VF.deltaV = vectorScale(vectorAdd(VF.bl, VF.ul, 0), 1/(map["imsize"][1]-1));
    return VF;
}

void print_map(std::map<std::string, std::vector<double>> map, std::string keywords[15]){
    for(int i=0; i<15; i++){
        std::cout << keywords[i] << ": ";
        printVector(map[keywords[i]]);
    }
}

Pixel applyTexture(Shape triangle){

}
