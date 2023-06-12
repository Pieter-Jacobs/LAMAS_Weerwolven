# Players

-   A set of *n* agents
    *A* = {*a*<sub>1</sub>, *a*<sub>2</sub>, ..., *a*<sub>*n*</sub>}
    containing:

    -   a set of *v* villagers
        *V* = {*a*<sub>*i*</sub> ∈ *A* \| agent *i* is a villager}

    -   a set of *m* mafia
        *V* = {*a*<sub>*i*</sub> ∈ *A* \| agent *i* is a mafioso}

    -   a set of *d* detectives
        *V* = {*a*<sub>*i*</sub> ∈ *A* \| agent *i* is a detective}

-   Social parameter: each agent has a unique `social_stat` chance of
    talking to another agent during a day phase (with
    0≤`social_stat` ≤ 1)

-   During each game, a pre-defined number of players are randomly
    picked from the set of players. By design, these players are assumed
    to act suspiciously and can be observed as being suspicious by
    talking with them.

-   Every public announcement by players is assumed to be truthful
    (including those by mafia).

# Types of knowledge

-   Agent *i* is a mafioso: *Maf*<sub>*i*</sub>

-   Agent *i* is a detective: *Det*<sub>*i*</sub>

-   Agent *i* has been killed: *Dead*<sub>*i*</sub>

-   Agent *i* is acting suspiciously: *Sus*<sub>*i*</sub>

# Reasoning rules

-   Talking with suspicious players: if agent *i* talks with agent *j*
    and agent *j* acts suspiciously, then agent *i* knows that agent *j*
    is acting suspiciously.

    (*a*<sub>*i*</sub> talks with
    *a*<sub>*j*</sub> ∧ *Sus*<sub>*j*</sub>)
     → *K*<sub>*i*</sub>*Sus*<sub>*j*</sub>

-   Mafia knows who are mafia: if agent *i* and *j* are both mafia, then
    agent *i* knows agent *j* is a mafioso.

    (*Maf*<sub>*i*</sub>∧*Maf*<sub>*j*</sub>) → *K*<sub>*i*</sub>*Maf*<sub>*j*</sub>

-   Suspicious players possibly being mafia: if agent *i* knows that
    agent *j* is acting suspiciously, then agent *i* considers it to be
    possible that agent *j* is a mafioso:

    *K*<sub>*i*</sub>*Sus*<sub>*j*</sub> → *M*<sub>*i*</sub>*Maf*<sub>*j*</sub>

# Simulation design

-   Parameters:

    -   the number of villagers *v*

    -   the number of mafia *m*

    -   the number of detective *d*

    -   the number of talking rounds in a day phase `nr_of_talks`

    -   the probability distribution of values for `social_stat` for
        each player

    -   the number of non-mafia players that are acting suspiciously
        `nr_of_sus` (with 0≤ `nr_of_sus`  ≤ (*n*−*m*))

-   Talking rounds:

    During a talking round, half of the players are randomly picked to
    start talks. Each of these players uses their `social_stat` as the
    probability of whether they want to have a talk during that round.
    If the player does want to talk, they invite another randomly picked
    player to talk with. If the invited player also wants to talk (based
    on their `social_stat`), the talk between these two players starts.
    Now, the reasoning rules can be applied, such that the knowledge
    base can be extended.

-   Run of one game of Mafia:

    1.  Initialization of players:

        -   The pool of players is generated: *v* villagers, *m* mafia
            and *d* detectives

        -   For each player, the value for `social_stat` is generated
            through the `social_stat` distribution.

        -   From the pool of players, `nr_of_sus` players are randomly
            picked, such that agent *i*

    2.  Initial day phase: `nr_of_talks` talking rounds are done, but no
        voting happens yet.

    3.  **Night phase**:

        1.  Detectives randomly pick one player (which they have not
            checked out before) and gain the knowledge of whether that
            player is a mafioso: f.e. if agent *i* is a detective and
            they check out agent *j*, the knowledge extends with
            *K*<sub>*i*</sub>*Maf*<sub>*j*</sub> (if agent *j* is a
            mafioso) or *K*<sub>*i*</sub>¬*Maf*<sub>*j*</sub> (if
            agent *j* isn’t a mafioso).

        2.  The mafia generate a list of living players that know that
            they are suspicious (f.e. for each mafioso *i*, agent *j* is
            added to the list if
            *K*<sub>*i*</sub>*K*<sub>*j*</sub>*Sus*<sub>*i*</sub> ∧ ¬*Dead*<sub>*j*</sub>).
            From this list, they pick one random player *i* to kill,
            thus the knowledge extends with *Dead*<sub>*i*</sub>.
            If the list is empty, a random living non-mafia player is
            picked.

    4.  **Day phase**:

        1.  *Announcement phase*: The player *i* who was killed during
            the night phase is publicly announced:
            *Dead*<sub>*i*</sub>.

            <u>The game ends and is won by the mafia</u> if there are
            more living mafia than living non-mafia players remaining.

        2.  *Discussion phase*: `nr_of_talks` talking rounds are done,
            during which reasoning rules are applied.

        3.  *Voting phase*: Each non-mafia player generates a list of
            living players that they know are suspicious (f.e. for each
            non-mafia player *i*, agent *j* is added to their list if
            *K*<sub>*i*</sub>*Sus*<sub>*j*</sub> ∧ ¬*Dead*<sub>*j*</sub>).
            If the player’s list is empty, a random living player added
            to their list. Similarly, each mafioso generates a list of
            living players that know that they are suspicious (f.e. for
            each mafioso *i*, agent *j* is added to the list if
            *K*<sub>*i*</sub>*K*<sub>*j*</sub>*Sus*<sub>*i*</sub> ∧ ¬*Dead*<sub>*j*</sub>).
            If the mafioso’s list is empty, a random non-mafia living
            player added to their list.

            Then, all players pick a random player from their list that
            they want to vote to kill. The player *i* with the most
            votes is killed: *Dead*<sub>*i*</sub>. If there is a
            tie, a randomly picked player from the tie is killed.

            <u>The game ends and is won by the mafia</u> if there are
            more living mafia than living non-mafia players remaining.

            <u>The game ends and is won by the non-mafia players</u> if
            all the mafia are killed.