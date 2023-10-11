set(SRC
    norbit_wbms.c
    sbd.c
    sonarparse.c
    )

set(HDR    
    norbit_wbms.h
    sbd.h
    )

set(PUBLIC_HDR
    sonarparse.h
    )

target_sources(${TARGET_LIB}
    PRIVATE ${SRC} ${HDR}
    PUBLIC ${PUBLIC_HDR}
)