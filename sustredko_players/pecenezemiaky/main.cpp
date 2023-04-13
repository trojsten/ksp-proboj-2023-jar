#include "common.h"
#include <ranges>
#include <algorithm>
#include <complex>
using namespace std;

#define NAME "cpp"
#define COLOR "00ff00"

World world;


template<class T>
bool cmp(const T &a, const T&b) {
    return abs(complex<long double>(a.position.x - world.players[0].position.x, a.position.y - world.players[0].position.y)) < abs(complex<long double>(b.position.x - world.players[0].position.x, b.position.y - world.players[0].position.y));
}


optional<Coordinates> vratPosition()
{
    if (world.players.size() == 1)
    {
        return nullopt;
    }
    else 
    {
        sort(world.players.begin()+1, world.players.end(),cmp<Player>);
        return world.players[1].position;
    }
}


float checkUhol(double a, double b)
{
    double x_entity, x_player, y_entity, y_player;
    x_entity = a;
    y_entity = b;
    x_player = world.players[0].position.x;
    y_player = world.players[0].position.y;

    float uhol = 0;
    uhol = arg(complex<double>(x_entity-x_player,y_entity-y_player));
    return uhol;
};
std::vector<Coordinates> zleHuly()
{
    std::vector<Coordinates> nechod;
    float r = 0;
    Coordinates start;
    Coordinates end;
    Coordinates vektor;
    for (int i=0; i < world.bullets.size(); i++)
    {
        r = world.bullets[i].radius;
        start = world.bullets[i].position;
        end = world.bullets[i].position + world.bullets[i].velocity;
        vektor = world.bullets[i].velocity;
        nechod.push_back({checkUhol(start.x, start.y), checkUhol(end.x, end.y)});
        /*if (vzdialenost(start.x, start.y) < world.stat_values[int(Stat::Speed)] + r)
        {
            nechod.pushback(checkUhol(start.x, start.y),0);
            if (vzdialenost(end.x, end.y) < world.stat_values[int(Stat::Speed)] + r)
            {
                nechod[nechod.size()]=(checkUhol(start.x, start.y),(end.x, end.y));
            }
        }
        else if ((vzdialenost(end.x, end.y) < world.stat_values[int(Stat::Speed)] + r))
        {
            nechod.pushback(0,checkUhol(end.x, end.y));
        }
        else{
            //sem ta vec od Viki
*/

        }
    return nechod;
    }





// sem pis svoj kod
Command do_turn() 
{
    Player &myself = world.players[world.my_id];
    Command command;
    Coordinates hovno;
    //strelba
    if (vratPosition())
    {
        if ((abs(world.players[1].position.x - world.players[0].position.x) + 10 )< world.stat_values[(int)Stat::Range])
        {
            command.shoot = ShootType::OneBullet;
            float uhol  = checkUhol(world.players[1].position.x, world.players[1].position.y);
            command.angle = uhol;
        }
        else if (vratPosition() && (abs(complex<long double>(world.players[1].position.x - world.players[0].position.x, world.players[1].position.y - world.players[0].position.y))) < world.stat_values[int(Stat::BulletSpeed)])
        {
            hovno = { - (world.players[1].position.x - world.players[0].position.x), - (world.players[1].position.y - world.players[0].position.y)};
            float hnacka=checkUhol(hovno.x, hovno.y);
            int hovadinaNajvecsia = 0;
            for (int SakraDoPrdele = 0; SakraDoPrdele < world.bullets.size(); SakraDoPrdele++){
                if ((hnacka > zleHuly()[hovadinaNajvecsia].x && hnacka < zleHuly()[hovadinaNajvecsia].y) || (hnacka < zleHuly()[hovadinaNajvecsia].x && hnacka > zleHuly()[hovadinaNajvecsia].y)){
                    break;
                }
                else{
                    command.new_position  = hovno;
                }
                hovadinaNajvecsia=hovadinaNajvecsia+1;}
        }
    }
    else 
    {
        ranges::sort(world.entities, cmp<Entity>);
        command.shoot = ShootType::OneBullet;
        float uhol  = checkUhol(world.entities[0].position.x, world.entities[0].position.y);
        command.angle = uhol;
    }
    //pohyb
    int zachrana = 0;
    vector<pair<double,double>> steny = {{abs(world.max_x - world.players[0].position.x),0},{abs(world.min_x - world.players[0].position.x),2},{abs(world.min_y-world.players[0].position.y),1},{abs(world.max_y-world.players[0].position.y),3}};
    int ste = 0;
    while (ste < 4)
    {
        if (steny[ste].first < 150)
        {
            zachrana=1;
        };
        ste = ste + 1;
    };
    if (world.entities.size() == 0 or zachrana > 0) 
    {
        hovno = { (world.max_x + world.min_x) / 2 - world.players[0].position.x, (world.max_y + world.min_y) / 2 - world.players[0].position.y};
        float hnacka=checkUhol(hovno.x, hovno.y);
            int hovadinaNajvecsia = 0;
            for (int SakraDoPrdele = 0; SakraDoPrdele < world.bullets.size(); SakraDoPrdele++){
                if ((hnacka > zleHuly()[hovadinaNajvecsia].x && hnacka < zleHuly()[hovadinaNajvecsia].y) || (hnacka < zleHuly()[hovadinaNajvecsia].x && hnacka > zleHuly()[hovadinaNajvecsia].y)){
                    break;
                }
                else{
                    command.new_position  = hovno;
                }
                hovadinaNajvecsia=hovadinaNajvecsia+1;}
    }    
    else if (abs(complex<long double>(world.entities[0].position.x - world.players[0].position.x, world.entities[0].position.y - world.players[0].position.y)) < (50 + 2 * world.stat_values[(int)Stat::Speed]))
    {
        hovno = { - world.entities[0].position.y + world.players[0].position.y, world.entities[0].position.x - world.players[0].position.x};
        float hnacka=checkUhol(hovno.x, hovno.y);
            int hovadinaNajvecsia = 0;
            for (int SakraDoPrdele = 0; SakraDoPrdele < world.bullets.size(); SakraDoPrdele++){
                if ((hnacka > zleHuly()[hovadinaNajvecsia].x && hnacka < zleHuly()[hovadinaNajvecsia].y) || (hnacka < zleHuly()[hovadinaNajvecsia].x && hnacka > zleHuly()[hovadinaNajvecsia].y)){
                    break;
                }
                else{
                    command.new_position  = hovno;
                }
                hovadinaNajvecsia=hovadinaNajvecsia+1;}
   }  
    else
    {
        hovno = {world.entities[0].position.x - world.players[0].position.x, world.entities[0].position.y - world.players[0].position.y};
        float hnacka=checkUhol(hovno.x, hovno.y);
            int hovadinaNajvecsia = 0;
            for (int SakraDoPrdele = 0; SakraDoPrdele < world.bullets.size(); SakraDoPrdele++){
                if ((hnacka > zleHuly()[hovadinaNajvecsia].x && hnacka < zleHuly()[hovadinaNajvecsia].y) || (hnacka < zleHuly()[hovadinaNajvecsia].x && hnacka > zleHuly()[hovadinaNajvecsia].y)){
                    break;
                }
                else{
                    command.new_position  = hovno;
                }
                hovadinaNajvecsia=hovadinaNajvecsia+1;}
    }
    
    //level ups
    if (world.stat_levels[(int)Stat::Range] <= 1)
    {
        command.stat = Stat::Range;
    }
    else if (world.stat_levels[(int)Stat::BulletTTL] <= 2)
    {
        command.stat = Stat::BulletTTL;
    }
    else if (world.stat_levels[(int)Stat::Speed] <= 2)
    {
        command.stat = Stat::Speed;

    }
    if (world.stat_levels[(int)Stat::Range] <= 5)
    {
        command.stat = Stat::Range;
    }
    else if (world.stat_levels[(int)Stat::ReloadSpeed] <= 6)
    {
        command.stat = Stat::ReloadSpeed;
    }
    else if (world.stat_levels[(int)Stat::BulletTTL] <= 5)
    {
        command.stat = Stat::BulletTTL;
    }
    else if (world.stat_levels[(int)Stat::BulletDamage] <= 3 || world.stat_levels[(int)Stat::HealthRegeneration] <= 2) 
    {
        if (world.stat_levels[(int)Stat::BulletDamage] < world.stat_levels[(int)Stat::HealthRegeneration] + 1)
        {
            command.stat = Stat::BulletDamage;
        }
        else
        {
            command.stat = Stat::HealthRegeneration;
        }
    }
    else if (world.stat_levels[(int)Stat::BulletDamage] <= 6 || world.stat_levels[(int)Stat::HealthMax] <= 3) 
    {
        if (world.stat_levels[(int)Stat::BulletDamage]+2 < world.stat_levels[(int)Stat::HealthRegeneration])
        {
            command.stat = Stat::BulletDamage;
        }
        else
        {
            command.stat = Stat::HealthRegeneration;
        }
    }

    //leveling tank
    if( world.level >= 10)
    {
        command.new_tank_id = Tank::Sniper;
    }
    
    cerr << world.level << "\n";
    if (world.players[0].tankType == Tank::Sniper)
    {
        cerr << "Ja uz som velky tank" << '\n';
        cerr << command.new_position << "\n";
    }

    return command;
}

int main() 
{
    // aby sme mali nahodu
    srand(time(nullptr));
    // robime tahy kym sme zivy
    do {
        cin >> world;
        cout << do_turn();
    } while (true);
    //cout << "Bye\n";
}

