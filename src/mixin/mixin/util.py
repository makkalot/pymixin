'''
    Created on Nov 10, 2011
    @author: makkalot

'''
import sys

try:
    from types import ClassType
    __python3 = False
except ImportError:
    __python3 = True


def wrap_class_meta(callback, depth=2):
    frame = sys._getframe(depth)
    caller_locals, caller_globals = frame.f_locals, frame.f_globals
    
    #print "%s - %s "%(caller_locals, caller_globals)
    
    prev_meta_class = caller_locals.get('__metaclass__')
    if __python3:
        default_meta_class  = caller_globals.get('__metaclass__', type)
    else:
        default_meta_class  = caller_globals.get('__metaclass__', ClassType)


    def advise(name, bases, cdict):

        if '__metaclass__' in cdict:
            del cdict['__metaclass__']
        if prev_meta_class is None:
            if bases:
                # find best metaclass or use global __metaclass__ if no bases
                meta = determine_meta_class(bases)
            else:
                meta = default_meta_class

        else:
            meta = determine_meta_class(bases, prev_meta_class)

        new_class = meta(name,bases,cdict)

        # this lets the callback replace the class completely, if it wants to
        return callback(new_class)

    # install the advisor
    caller_locals['__metaclass__'] = advise
    

def determine_meta_class(bases, explicit_mc=None):
    """Determine metaclass from 1+ bases and optional explicit __metaclass__"""

    meta = [getattr(b,'__class__',type(b)) for b in bases]

    if explicit_mc is not None:
        # The explicit metaclass needs to be verified for compatibility
        # as well, and allowed to resolve the incompatible bases, if any
        meta.append(explicit_mc)

    if len(meta)==1:
        # easy case
        return meta[0]

    candidates = minimal_bases(meta) # minimal set of metaclasses

    if not candidates:
        # they're all "classic" classes
        assert(not __python3) # This should not happen under Python 3
        return ClassType

    elif len(candidates)>1:
        # We could auto-combine, but for now we won't...
        raise TypeError("Incompatible metatypes",bases)

    # Just one, return it
    return candidates[0]


def minimal_bases(classes):
    """Reduce a list of base classes to its ordered minimum equivalent"""

    if not __python3:
        classes = [c for c in classes if c is not ClassType]
    candidates = []

    for m in classes:
        for n in classes:
            if issubclass(n,m) and m is not n:
                break
        else:
            # m has no subclasses in 'classes'
            if m in candidates:
                candidates.remove(m)    # ensure that we're later in the list
            candidates.append(m)

    return candidates

