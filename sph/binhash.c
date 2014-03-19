#include <string.h>

#include "zmorton.h"
#include "binhash.h"

/*@q
 * ====================================================================
 */

/*@T
 * \subsection{Spatial hashing implementation}
 * 
 * In the current implementation, we assume [[HASH_DIM]] is $2^b$,
 * so that computing a bitwise of an integer with [[HASH_DIM]] extracts
 * the $b$ lowest-order bits.  We could make [[HASH_DIM]] be something
 * other than a power of two, but we would then need to compute an integer
 * modulus or something of that sort.
 * 
 *@c*/

#define HASH_MASK (HASH_DIM-1)

unsigned particle_bucket(particle_t* p, float h)
{
    unsigned ix = p->x[0]/h;
    unsigned iy = p->x[1]/h;
    unsigned iz = p->x[2]/h;
    return zm_encode(ix & HASH_MASK, iy & HASH_MASK, iz & HASH_MASK);
}

unsigned particle_neighborhood(unsigned* buckets, particle_t* p, float h)
{
    /* BEGIN TASK */
    unsigned pb = particle_bucket(p, h);
    unsigned x,y,z;
    zm_decode(pb, &x, &y, &z);
    unsigned count = 0;
    buckets[count] = zm_encode((x)&HASH_MASK, (y)&HASH_MASK, (z)&HASH_MASK);
		    				
    for(int iz = -1; iz <= 1; iz++){
	    for(int iy = -1; iy <= 1; iy++){
			for(int ix = -1; ix <= 1; ix++){
				int bk = zm_encode(((unsigned)(x+ix))&HASH_MASK, ((unsigned)(y+iy))&HASH_MASK, ((unsigned)(z+iz))&HASH_MASK);
				if(0 <= bk && bk < HASH_SIZE){
					buckets[count] = bk;
					count++;
				}
	    	}
	    }
    }

    return count;

    /* END TASK */
}

void hash_particles(sim_state_t* s, float h)
{
    /* BEGIN TASK */
    for(int i = 0; i < HASH_SIZE; i++){
    	s->hash[i] = NULL;
    }
    for(int i = 0; i < s->n; i++){
    	particle_t * pi = s->part + i;
    	unsigned pb = particle_bucket(pi, h);
    	pi->next = s->hash[pb];
    	s->hash[pb] = pi;
    }
    /* END TASK */
}
