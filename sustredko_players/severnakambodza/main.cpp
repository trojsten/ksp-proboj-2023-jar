#include "common.h"
#include <experimental/random>

using namespace std;

World world;
long long tick = 0;

std::vector<Coordinates> prev_positions;

auto compute_velocity() -> void
{
    std::vector<long double> velocities(prev_positions.size());
    for (int i = 0; auto& p : world.players) {
        velocities[i] =
            std::sqrt(std::pow(prev_positions[i].x - p.position.x, 2) +
                      std::pow(prev_positions[i].y - p.position.y, 2));
        ++i;
    }
}

// sem pis svoj kod
Command do_turn()
{
    ++tick;
    Player& myself = world.players[0];
    Command command;

    Coordinates nearest{1000000, 1000000};
    for (auto& e : world.entities) {
        if (distance(myself.position, e.position) <
            distance(myself.position, nearest)) {
            nearest = e.position;
        }
    }

    for (auto& p : world.players) {
        if (p.id == myself.id)
            continue;
        if (distance(myself.position, p.position) <
            distance(myself.position, nearest)) {
            nearest = p.position;
        }
    }


    std::cerr << nearest << '\n';
    std::cerr << myself.position << '\n';
    auto v               = nearest - myself.position;
    command.angle        = atan2(v.y, v.x);
    command.shoot        = ShootType::OneBullet;
    command.new_position = nearest;
    command.stat         = Stat::ReloadSpeed;

    if (myself.updatable_to.size()) {
        command.new_tank_id = myself.updatable_to[1];
    }

    std::cerr << command << '\n';
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
    // cout << "Bye\n";
}


//    if (tick % 2) {
//        command.follow_coordinates = {};
//    }
//    else {
//    }
//
//    for (int i = 0; auto& p : world.players) {
//        prev_positions[i++] = p.position;
//    }

